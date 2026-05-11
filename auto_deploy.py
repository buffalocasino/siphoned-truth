#!/usr/bin/env python3
"""Auto-commit, image-generate, and Vercel deploy for siphoned-truth blog."""
import subprocess, json, shutil, urllib.request, time
from pathlib import Path
from datetime import datetime

BLOG = Path("/home/trevo/blog")
COVERS = BLOG / "static" / "covers"
COVERS.mkdir(parents=True, exist_ok=True)

# Track processed slugs so we don't re-generate images on every run
PROCESSED_MARKER = BLOG / ".deployed_slugs"

MINIMAX_MEDIA_KEY = 'sk-cp-iwiL6pOy3nspdEU5U-a0v6wrSKxo06qIBf8GsagrC7yx6TIIq6vf7x7c2ay09lOPbZ2S2jEnM4LPv0TeyElzqIoK3_9coTDkKeJIPZBJSG2Kjhahe1LD2tU'
GROUP_ID = '2038430040336634210'

CATEGORY_PROMPTS = {
    'aviation':    'Reuters-style investigative news photo, aviation accident runway investigation, dark moody airport tarmac emergency vehicles, cinematic documentary photography ultra-realistic, no text or overlays',
    'geopolitics': 'Reuters-style breaking news photo, diplomatic crisis capitol building tense political atmosphere overcast, war room press briefing cinematic documentary ultra-realistic, no text or overlays',
    'energy':      'Reuters-style news photo, oil refinery energy facility industrial complex at night dramatic sky, commodity trading cinematic documentary ultra-realistic, no text or overlays',
    'maritime':    'Reuters-style news photo, commercial tanker ship at sea Strait of Hormuz, naval vessels dramatic ocean storm lighting cinematic documentary ultra-realistic, no text or overlays',
    'default':     'Reuters-style breaking news photo, dark atmospheric news scene cinematic documentary ultra-realistic, no text or overlays',
}

def load_processed():
    if PROCESSED_MARKER.exists():
        return set(PROCESSED_MARKER.read_text().splitlines())
    return set()

def save_processed(slugs):
    PROCESSED_MARKER.write_text('\n'.join(sorted(slugs)))

def run(*args, cwd=BLOG, **kw):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(f"ERROR {' '.join(args)}: {r.stderr[:300]}")
        return False
    return True

def sync_articles():
    """Mirror content/articles/ → src/lib/articles/ (the glob source).
    Always overwrites to ensure deleted source = deleted destination."""
    src_dir = BLOG / "content" / "articles"
    dst_dir = BLOG / "src" / "lib" / "articles"
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Remove orphaned files (exist in dst but not in src)
    src_names = {f.name for f in src_dir.glob("*.json")}
    for f in dst_dir.glob("*.json"):
        if f.name not in src_names:
            f.unlink()
            print(f"  Removed stale: {f.name}")

    # Always overwrite — prevents stale copies from blocking new content
    count = 0
    for f in src_dir.glob("*.json"):
        dst = dst_dir / f.name
        shutil.copy2(f, dst)
        count += 1
    return count

def generate_cover(slug, title, category='default'):
    """Generate cover image via MiniMax image-01. Returns slug of saved file."""
    filename = f"{slug.lower()}.jpg"
    out_path = COVERS / filename
    if out_path.exists():
        print(f"  Cover exists: {filename}")
        return filename

    prompt_text = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS['default'])
    prompt = f"Dark OSINT journalist aesthetic: {title}. {prompt_text}"

    payload = json.dumps({
        'model': 'image-01',
        'prompt': prompt,
        'aspect_ratio': '16:9',
        'response_format': 'url',
        'n': 1
    }).encode()

    req = urllib.request.Request(
        'https://api.minimax.io/v1/image_generation',
        data=payload,
        headers={
            'Authorization': f'Bearer {MINIMAX_MEDIA_KEY}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        image_url = data['data']['image_urls'][0]
        print(f"  Generated cover: {image_url}")

        # Download and save
        urllib.request.urlretrieve(image_url, out_path)
        print(f"  Saved: {out_path} ({out_path.stat().st_size // 1024}KB)")
        return filename
    except Exception as e:
        print(f"  Cover generation failed for {slug}: {e}")
        return None

def validate_json(filepath):
    """Remove corrupt JSON files before staging."""
    try:
        json.load(open(filepath))
        return True
    except json.JSONDecodeError as e:
        print(f"  REMOVED CORRUPT: {filepath.name} — {e}")
        filepath.unlink()
        return False

def main():
    # 1. Sync articles (always overwrite to fix stale file bug)
    synced = sync_articles()
    if synced:
        print(f"Synced {synced} article(s) from content/articles/")

    # 2. Validate JSON files
    for f in (BLOG / "src/lib/articles").glob("*.json"):
        validate_json(f)

    # 3. Generate covers for new articles
    processed = load_processed()
    new_articles = []

    for f in (BLOG / "content/articles").glob("*.json"):
        try:
            article = json.load(open(f))
            slug = article.get('slug') or article.get('id', '')
            if slug and slug not in processed:
                title = article.get('title', '')
                category = article.get('category', 'default')
                result = generate_cover(slug, title, category)
                processed.add(slug)
                new_articles.append(slug)
        except Exception as e:
            print(f"  Skipping {f.name}: {e}")

    if new_articles:
        print(f"Generated {len(new_articles)} cover image(s): {new_articles}")
    save_processed(processed)

    # 4. Stage and commit
    result = subprocess.run(
        ["git", "status", "--porcelain", "-uall", "--", "src/", "static/covers/", ".deployed_slugs"],
        cwd=BLOG, capture_output=True, text=True
    )
    uncommitted = [l for l in result.stdout.splitlines()
                  if l.startswith("??") or l.startswith(" M") or l.startswith(" D")]

    if not uncommitted:
        print("No new articles.")
        return

    new_count = len([l for l in uncommitted if l.startswith("??")])
    print(f"Staging {len(uncommitted)} file(s) ({new_count} new)")

    if not run("git", "add", "src/", "static/covers/", ".deployed_slugs"):
        return

    # Commit
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = f"auto-deploy {len(uncommitted)} files ({new_count} new articles) - {ts}"

    if not run("git", "commit", "-m", msg):
        return

    # Push to GitHub
    if not run("git", "push", "origin", "master"):
        print("GitHub push failed, continuing with Vercel deploy...")

    print("Committed + pushed. Deploying to Vercel...")

    # Vercel --prod deploy
    r = subprocess.run(
        ["npx", "vercel", "--prod", "--force"],
        cwd=BLOG, capture_output=True, text=True, timeout=180
    )
    if r.returncode != 0:
        print(f"Vercel deploy FAILED: {r.stderr[-300:]}")
        return

    # Extract URL from output
    for line in r.stdout.splitlines():
        if "https://blog-iota-gray-35.vercel.app" in line:
            print(f"✅ LIVE: {line.strip()}")
            break
    else:
        print(f"✅ Deploy complete: {r.stdout[-200:]}")

if __name__ == "__main__":
    main()