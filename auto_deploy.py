"""Auto-commit, image-generate, and Vercel deploy for siphoned-truth blog."""
import subprocess, json, shutil, urllib.request, time, os
from pathlib import Path
from datetime import datetime

# Resolve BLOG to the directory containing this script — works on WSL, Windows, native Linux
SCRIPT_DIR = Path(__file__).resolve().parent
BLOG = SCRIPT_DIR
COVERS = BLOG / "static" / "covers"
COVERS.mkdir(parents=True, exist_ok=True)

# Track processed slugs so we don't re-generate images on every run
PROCESSED_MARKER = BLOG / ".deployed_slugs"
FB_POSTS_DIR = BLOG / "static" / "fb-posts"

MINIMAX_MEDIA_KEY = os.environ.get('MINIMAX_KEY', 'sk-cp-iwiL6pOy3nspdEU5U-a0v6wrSKxo06qIBf8GsagrC7yx6TIIq6vf7x7c2ay09lOPbZ2S2jEnM4LPv0TeyElzqIoK3_9coTDkKeJIPZBJSG2Kjhahe1LD2tU')
OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY', '')
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
    # Resolve npm/node to absolute paths
    import shutil
    resolved = []
    for arg in args:
        if arg == "npm":
            resolved.append(shutil.which("npm") or "/home/trevo/.local/bin/npm")
        elif arg == "node":
            resolved.append(shutil.which("node") or "/home/trevo/.local/bin/node")
        elif arg == "npx":
            resolved.append(shutil.which("npx") or "/home/trevo/.local/bin/npx")
        else:
            resolved.append(arg)
    r = subprocess.run(resolved, cwd=cwd, capture_output=True, text=True, **kw)
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
    """Generate cover image via MiniMax image-01, falling back to OpenRouter Gemini."""
    filename = f"{slug.lower()}.jpg"
    out_path = COVERS / filename
    if out_path.exists():
        print(f"  Cover exists: {filename}")
        return filename

    prompt_text = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS['default'])
    prompt = f"Dark OSINT journalist aesthetic: {title}. {prompt_text}"

    # Tier 1: MiniMax image-01
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
        if data.get('data') and data['data'].get('image_urls'):
            image_url = data['data']['image_urls'][0]
            urllib.request.urlretrieve(image_url, out_path)
            print(f"  [MiniMax] Saved: {out_path} ({out_path.stat().st_size // 1024}KB)")
            return filename
        elif data.get('base_resp', {}).get('status_code') == 2056:
            print(f"  MiniMax quota exhausted for {slug}, trying OpenRouter...")
        else:
            print(f"  MiniMax API error for {slug}: {data.get('base_resp', {}).get('status_msg', 'unknown')}")
    except Exception as e:
        print(f"  MiniMax failed for {slug}: {e}")

    # Tier 2: OpenRouter Gemini
    if OPENROUTER_KEY:
        result = _generate_cover_openrouter(slug, prompt, out_path)
        if result:
            return result

    # Tier 3: Pillow local fallback (always available, zero API cost)
    return _generate_cover_pillow(slug, title, category, out_path)

def _generate_cover_openrouter(slug, prompt, out_path):
    """Fallback cover generation via OpenRouter Gemini image models."""
    import base64
    payload = json.dumps({
        'model': 'google/gemini-2.5-flash-image',
        'messages': [{'role': 'user', 'content': prompt}],
        'modalities': ['image', 'text'],
        'max_tokens': 4096
    }).encode()

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=payload,
        headers={
            'Authorization': f'Bearer {OPENROUTER_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://siphonedtruth.online',
            'X-Title': 'Siphoned Truth'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        images = data.get('choices', [{}])[0].get('message', {}).get('images', [])
        if not images:
            print(f"  Gemini returned no images for {slug}")
            return None

        img_url = images[0].get('image_url', {}).get('url', '')
        if img_url.startswith('data:'):
            header, b64 = img_url.split(',', 1)
            with open(out_path, 'wb') as f:
                f.write(base64.b64decode(b64))
        elif img_url.startswith('http'):
            urllib.request.urlretrieve(img_url, out_path)
        else:
            print(f"  Gemini unknown image format for {slug}")
            return None

        print(f"  [OpenRouter Gemini] Saved: {out_path} ({out_path.stat().st_size // 1024}KB)")
        return out_path.name
    except Exception as e:
        print(f"  Gemini failed for {slug}: {e}")
        return None

def _generate_cover_pillow(slug, title, category, out_path):
    """Tier 3: Local cover generation via Pillow — always available, zero API cost."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print(f"  Pillow not installed — cannot generate cover for {slug}")
        return None

    CAT_COLORS = {
        'aviation':    ((26, 26, 46), (233, 69, 96)),
        'geopolitics': ((26, 10, 10), (255, 107, 53)),
        'energy':      ((10, 26, 10), (0, 255, 136)),
        'maritime':    ((10, 10, 46), (0, 212, 255)),
        'default':     ((17, 17, 17), (0, 255, 136)),
    }

    def _wrap(text, font, max_w, draw):
        words = text.split()
        lines = []
        current = ''
        for w in words:
            test = current + ' ' + w if current else w
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    bg, accent = CAT_COLORS.get(category, CAT_COLORS['default'])
    img = Image.new('RGB', (1280, 720), bg)
    draw = ImageDraw.Draw(img)

    # Use Segoe UI (Windows system font, better readability than Arial)
    font_path = 'C:/Windows/Fonts/segoeui.ttf'
    try:
        title_font = ImageFont.truetype(font_path, 36)
        tag_font = ImageFont.truetype(font_path, 18)
        slug_font = ImageFont.truetype(font_path, 13)
    except OSError:
        font_path = 'C:/Windows/Fonts/arial.ttf'
        title_font = ImageFont.truetype(font_path, 36)
        tag_font = ImageFont.truetype(font_path, 18)
        slug_font = ImageFont.truetype(font_path, 13)

    # Draw text onto a separate RGBA layer for clean compositing (avoids JPEG artifacts on text)
    txt_layer = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_layer)

    # Wrap title with generous margins
    lines = _wrap(title, title_font, 880, txt_draw)
    if len(lines) > 4:
        lines = lines[:4]
        lines[-1] = lines[-1][:70] + '...'

    # Title — white, slightly transparent for depth
    line_h = 46
    total_h = len(lines) * line_h
    y = 290 - total_h // 2
    for i, line in enumerate(lines):
        bbox = txt_draw.textbbox((0, 0), line, font=title_font)
        tw = bbox[2] - bbox[0]
        # Subtle shadow for readability on any background
        txt_draw.text((640 - tw // 2 + 2, y + i * line_h + 2), line, fill=(0, 0, 0, 60), font=title_font)
        txt_draw.text((640 - tw // 2, y + i * line_h), line, fill=(255, 255, 255, 240), font=title_font)

    # Accent line
    line_y = y + total_h + 30
    txt_draw.line([(300, line_y), (980, line_y)], fill=accent + (200,), width=2)

    # Tag
    tag = 'THE SIPHONED TRUTH'
    bbox = txt_draw.textbbox((0, 0), tag, font=tag_font)
    tw = bbox[2] - bbox[0]
    txt_draw.text((640 - tw // 2 + 1, line_y + 40 + 1), tag, fill=(0, 0, 0, 40), font=tag_font)
    txt_draw.text((640 - tw // 2, line_y + 40), tag, fill=accent + (220,), font=tag_font)

    # Slug at bottom
    slug_text = f'siphonedtruth.online/article/{slug[:60]}'
    bbox = txt_draw.textbbox((0, 0), slug_text, font=slug_font)
    tw = bbox[2] - bbox[0]
    txt_draw.text((640 - tw // 2, 685), slug_text, fill=(180, 180, 180, 140), font=slug_font)

    # Composite text layer onto background, then convert to RGB for JPEG save
    img = Image.alpha_composite(img.convert('RGBA'), txt_layer).convert('RGB')

    img.save(str(out_path), 'JPEG', quality=85)
    print(f"  [Pillow] Saved: {out_path} ({out_path.stat().st_size // 1024}KB)")
    return out_path.name

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
                if result:
                    processed.add(slug)
                    new_articles.append(slug)
                else:
                    print(f"  Cover FAILED for {slug} — will retry next run")
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
        ["git", "status", "--porcelain", "-uall", "--", "src/", "content/", "static/covers/", "static/fb-posts/", ".deployed_slugs"],
        cwd=BLOG, capture_output=True, text=True
    )
    uncommitted = [l for l in result.stdout.splitlines()
                  if l.startswith("??") or l.startswith(" M") or l.startswith(" D")]

    if not uncommitted:
        print("No new articles.")
        return

    new_count = len([l for l in uncommitted if l.startswith("??")])
    print(f"Staging {len(uncommitted)} file(s) ({new_count} new)")

    if not run("git", "add", "src/", "content/", "static/covers/", "static/fb-posts/", ".deployed_slugs"):
        return

    # Commit
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = f"auto-deploy {len(uncommitted)} files ({new_count} new articles) - {ts}"

    if not run("git", "commit", "-m", msg):
        return

    # 1. Build via `vercel build` (not `npm run build`).
    #    npx vercel build writes the correct .vercel/output/config.json with
    #    version:3 (Build Output API v3). npm run build (vite) only populates
    #    the build/ directory and never touches .vercel/output/, leaving a
    #    stale config that fails deploys with "Expected version: 3".
    print("Building via vercel build...")
    if not run("npx", "vercel", "build", "--prod"):
        print("Build failed, aborting deploy.")
        return

# 1b-1d. Sync build artifacts to .vercel/output (required for --prebuilt deploy).
    # If .vercel/output/ doesn't exist yet, initialize it from the build output.
    vercel_static = BLOG / ".vercel/output/static"
    if not vercel_static.exists():
        print("  .vercel/output not found — initializing from build/")
        vercel_static.mkdir(parents=True, exist_ok=True)
        (BLOG / ".vercel/output/config.json").write_text('{"routes":[]}')

    # 1b. Sync covers from build/ to .vercel/output/static/
    #     SvelteKit's static adapter outputs to build/, but --prebuilt uploads
    #     from .vercel/output/static/. If covers were added since last deploy,
    #     they exist in build/ but not in .vercel/output/static/ → broken images.
    vercel_covers = vercel_static / "covers"
    build_covers  = BLOG / "build/covers"
    if build_covers.exists():
        vercel_covers.mkdir(parents=True, exist_ok=True)
        for f in build_covers.glob("*.jpg"):
            dest = vercel_covers / f.name
            if not dest.exists() or f.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(f, dest)

    # 1b2. Sync _app assets (JS/CSS) from build/ to .vercel/output/static/
    #      Without this, --prebuilt deploy ships without CSS/JS = unstyled page.
    build_app  = BLOG / "build/_app"
    vercel_app = vercel_static / "_app"
    if build_app.exists():
        for src_file in build_app.rglob("*"):
            if src_file.is_file():
                rel = src_file.relative_to(build_app)
                dst = vercel_app / rel
                if not dst.exists() or src_file.stat().st_mtime > dst.stat().st_mtime:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst)

    # 1b3. Sync root static files (logo.svg, favicon, etc.) from build/ to .vercel/output/static/
    #      These live at the site root but the static adapter puts them in build/.
    for name in ["logo.svg", "favicon.png", "og-default.jpg", "robots.txt"]:
        src = BLOG / "build" / name
        dst = vercel_static / name
        if src.exists():
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(src, dst)
        # Remove covers from .vercel/output that no longer exist in build/
        for f in vercel_covers.glob("*.jpg"):
            if not (build_covers / f.name).exists():
                f.unlink()

    # 1c. Sync pre-rendered article HTML from build/ to .vercel/output/static/
    #     The article pages are pre-rendered with correct slug-based cover paths.
    #     Without this sync the old HTML (with id-based paths) gets uploaded.
    vercel_article = vercel_static / "article"
    build_article  = BLOG / "build/article"
    if build_article.exists():
        vercel_article.mkdir(parents=True, exist_ok=True)
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
        dst = vercel_static / name
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
        # CRITICAL: Replace ALL routes — do not merge. vercel build produces a
        # catchall "status: 404" at position 0 that would shadow the article
        # rewrite if preserved. Correct order: specific → filesystem → catchall.
        cfg = {"version": 3, "routes": [
            {"src": r"^/covers/(.*)$", "dest": "/covers/$1"},
            {"src": r"^/_app/(.*)$", "dest": "/_app/$1"},
            {"src": r"^/article/([^/]+)$", "dest": "/article/$1.html"},
            {"handle": "filesystem"},
            {"src": r"^(?!/api).*$", "status": 404, "dest": "/404.html"},
        ]}
        vercel_config.write_text(json.dumps(cfg, indent=2))
        print("Rewrote Vercel routing config with proper /article/{slug} → .html mapping")

    # 3. Push to GitHub
    if not run("git", "push", "origin", "master"):
        print("GitHub push failed, continuing with Vercel deploy...")

    print("Pushed. Deploying to Vercel (--prebuilt)...")

    # Vercel --prod deploy with --prebuilt to bypass server-side build
    # BUG FIX: --prebuilt uploads the pre-rendered static output without
    # triggering a serverless build. The old --force path ran `npm run build`
    # on Vercel's servers which hit size/compute limits on this project.
    # BUG FIX 2: --archive=tgz avoids the 5000-file upload limit on
    # static-heavy projects. Without it, Vercel counts every file and
    # rejects deploys with "Too many requests - try again in 24 hours
    # (more than 5000, code: api-upload-free)".
    r = run("npx", "vercel", "--prod", "--prebuilt", "--yes", "--archive=tgz")
    if not r:
        print("Vercel deploy FAILED (non-zero exit)")
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