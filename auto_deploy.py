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
FB_POSTS_DIR = BLOG / "static" / "fb-posts"

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

def generate_fb_post(article):
    """Generate a ready-to-paste Facebook post for an article."""
    title = article.get('title', '')
    narrative = article.get('narrative', '')
    verdict = article.get('verdict', '')
    category = article.get('category', 'OSINT')
    slug = article.get('slug', article.get('id', ''))
    url = f"https://siphonedtruth.online/article/{slug}"

    first_sentence = narrative.split('.')[0] + '.' if narrative else ''
    if verdict.startswith('[SIPHONED VERDICT]:'):
        verdict = verdict[len('[SIPHONED VERDICT]:'):].strip()
    elif verdict.startswith('[SIPHONED VERDICT]'):
        verdict = verdict[len('[SIPHONED VERDICT]'):].strip()

    lines = [
        f"⬡ {title}",
        "",
        f"{first_sentence}",
        "",
        "The telemetry doesn't lie.",
        "",
        f"▸ {verdict}",
        "",
        f"→ {url}",
        "",
        "#SiphonedTruth #OSINT #ShadowBroker",
    ]
    return '\n'.join(lines)

def validate_json(filepath):
    """Remove corrupt JSON files before staging."""
    try:
        json.load(open(filepath))
        return True
    except json.JSONDecodeError as e:
        print(f"  REMOVED CORRUPT: {filepath.name} — {e}")
        filepath.unlink()
        return False

def validate_verdict(filepath):
    """Flag articles missing or lacking proper [SIPHONED VERDICT]: prefix."""
    try:
        d = json.load(open(filepath))
        verdict = d.get('verdict', '')
        if not verdict:
            print(f"  MISSING VERDICT: {filepath.name}")
            return False
        if not verdict.startswith('[SIPHONED VERDICT]'):
            print(f"  MISSING PREFIX: {filepath.name} — verdict: {verdict[:50]}")
            return False
        return True
    except:
        return False

def main():
    # 1. Sync articles (always overwrite to fix stale file bug)
    synced = sync_articles()
    if synced:
        print(f"Synced {synced} article(s) from content/articles/")

    # 2. Validate JSON files and verdict format
    bad_verdicts = []
    for f in (BLOG / "src/lib/articles").glob("*.json"):
        validate_json(f)
        if not validate_verdict(f):
            bad_verdicts.append(f.name)

    if bad_verdicts:
        print(f"WARNING: {len(bad_verdicts)} article(s) with bad/missing verdicts — fix before publishing:")
        for name in bad_verdicts:
            print(f"  {name}")

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

    # 3b. Generate FB post drafts for new articles
    FB_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    new_fb_posts = []
    for slug in new_articles:
        # find the article file
        for f in (BLOG / "content/articles").glob("*.json"):
            try:
                article = json.load(open(f))
                if article.get('slug') == slug or article.get('id', '').lower() == slug:
                    post = generate_fb_post(article)
                    out_path = FB_POSTS_DIR / f"{slug}.txt"
                    out_path.write_text(post)
                    new_fb_posts.append(slug)
                    break
            except:
                pass

    if new_fb_posts:
        print(f"Generated {len(new_fb_posts)} FB post draft(s): {new_fb_posts}")

    # 4. Stage and commit
    result = subprocess.run(
        ["git", "status", "--porcelain", "-uall", "--", "src/", "static/covers/", "static/fb-posts/", ".deployed_slugs"],
        cwd=BLOG, capture_output=True, text=True
    )
    uncommitted = [l for l in result.stdout.splitlines()
                  if l.startswith("??") or l.startswith(" M") or l.startswith(" D")]

    if not uncommitted:
        print("No new articles.")
        return

    new_count = len([l for l in uncommitted if l.startswith("??")])
    print(f"Staging {len(uncommitted)} file(s) ({new_count} new)")

    if not run("git", "add", "src/", "static/covers/", "static/fb-posts/", ".deployed_slugs"):
        return

    # Commit
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = f"auto-deploy {len(uncommitted)} files ({new_count} new articles) - {ts}"

    if not run("git", "commit", "-m", msg):
        return

    # 1. Build locally (required for --prebuilt flag)
    print("Building locally...")
    if not run("npm", "run", "build"):
        print("Local build failed, aborting deploy.")
        return

    # 1b. Sync covers from build/ to .vercel/output/static/
    #     SvelteKit's static adapter outputs to build/, but --prebuilt uploads
    #     from .vercel/output/static/. If covers were added since last deploy,
    #     they exist in build/ but not in .vercel/output/static/ → broken images.
    vercel_covers = BLOG / ".vercel/output/static/covers"
    build_covers  = BLOG / "build/covers"
    if build_covers.exists() and vercel_covers.exists():
        for f in build_covers.glob("*.jpg"):
            dest = vercel_covers / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)
        # Remove covers from .vercel/output that no longer exist in build/
        for f in vercel_covers.glob("*.jpg"):
            if not (build_covers / f.name).exists():
                f.unlink()

    # 1c. Sync pre-rendered article HTML from build/ to .vercel/output/static/
    #     The article pages are pre-rendered with correct slug-based cover paths.
    #     Without this sync the old HTML (with id-based paths) gets uploaded.
    vercel_article = BLOG / ".vercel/output/static/article"
    build_article  = BLOG / "build/article"
    if build_article.exists() and vercel_article.exists():
        for f in build_article.glob("*.html"):
            dest = vercel_article / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)
        for f in vercel_article.glob("*.html"):
            if not (build_article / f.name).exists():
                f.unlink()
        for f in build_article.glob("*.html.br"):
            dest = vercel_article / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)
        for f in build_article.glob("*.html.gz"):
            dest = vercel_article / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)

    # 1d. Sync root index.html (homepage card grid with correct slug-based cover URLs)
    for name in ["index.html", "index.html.br", "index.html.gz"]:
        src = BLOG / "build" / name
        dst = BLOG / ".vercel/output/static" / name
        if src.exists():
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)

# 2. Patch .vercel/output/config.json to route /article/{slug} → .html files
    #    Without this, Vercel routes /article/foo to /article/[slug] (SvelteKit
    #    filesystem route) which doesn't exist on the static host → 404.
    #    The .html files exist at /article/foo.html — this rewrites the route
    #    dest from the placeholder token to the actual file.
    vercel_config = BLOG / ".vercel/output/config.json"
    if vercel_config.exists():
        import re
        cfg = vercel_config.read_text()
        cfg = cfg.replace('"dest": "/article/[slug]"', '"dest": "/article/$1.html"')
        cfg = cfg.replace('"dest": "/fb-posts/[slug]"', '"dest": "/fb-posts/$1.txt"')
        vercel_config.write_text(cfg)
        print("Patched Vercel routing config: /article/{slug} → .html")

    # 3. Push to GitHub
    if not run("git", "push", "origin", "master"):
        print("GitHub push failed, continuing with Vercel deploy...")

    print("Pushed. Deploying to Vercel (--prebuilt)...")

    # Vercel --prod deploy with --prebuilt to bypass server-side build
    # BUG FIX: --prebuilt uploads the pre-rendered static output without
    # triggering a serverless build. The old --force path ran `npm run build`
    # on Vercel's servers which hit size/compute limits on this project.
    r = subprocess.run(
        ["npx", "vercel", "--prod", "--prebuilt", "--yes"],
        cwd=BLOG, capture_output=True, text=True, timeout=180
    )
    if r.returncode != 0:
        print(f"Vercel deploy FAILED: {r.stderr[-500:]}")
        return

    # Extract URL from output
    for line in r.stdout.splitlines():
        if "vercel.app" in line and "Completing" in r.stdout:
            # New project alias: siphonedtruth.online
            print(f"✅ LIVE: https://siphonedtruth.online")
            break
    else:
        print(f"✅ Deploy complete: {r.stdout[-300:]}")

if __name__ == "__main__":
    main()