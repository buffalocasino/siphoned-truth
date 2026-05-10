#!/usr/bin/env python3
"""Auto-commit and Vercel deploy for siphoned-truth blog."""
import subprocess, json
from pathlib import Path
from datetime import datetime

BLOG = Path("/home/trevo/blog")

def run(*args, cwd=BLOG, **kw):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(f"ERROR {' '.join(args)}: {r.stderr[:300]}")
        return False
    return True

def sync_articles():
    """Mirror content/articles/ → src/lib/articles/ (the glob source).
    Removes orphaned files in dst that no longer exist in src."""
    src_dir = BLOG / "content" / "articles"
    dst_dir = BLOG / "src" / "lib" / "articles"
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Remove orphaned files (exist in dst but not in src)
    src_names = {f.name for f in src_dir.glob("*.json")}
    for f in dst_dir.glob("*.json"):
        if f.name not in src_names:
            f.unlink()

    # Copy/update from src
    count = 0
    for f in src_dir.glob("*.json"):
        dst = dst_dir / f.name
        if not dst.exists() or dst.stat().st_mtime < f.stat().st_mtime:
            import shutil
            shutil.copy2(f, dst)
            count += 1
    return count

def main():
    # Sync content/articles/ → src/lib/articles/ first
    synced = sync_articles()
    if synced:
        print(f"Synced {synced} article(s) from content/articles/")

    # Stage articles from src/lib/articles/ (the actual article store)
    result = subprocess.run(
        ["git", "status", "--porcelain", "-uall", "--", "src/"],
        cwd=BLOG, capture_output=True, text=True
    )
    uncommitted = [l for l in result.stdout.splitlines()
                  if l.startswith("??") or l.startswith(" M")]

    if not uncommitted:
        print("No new articles.")
        return

    new_count = len([l for l in uncommitted if l.startswith("??")])
    print(f"Staging {len(uncommitted)} article(s) ({new_count} new)")

    if not run("git", "add", "src/"):
        return

    # Commit
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = f"auto-deploy {len(uncommitted)} articles ({new_count} new) - {ts}"

    if not run("git", "commit", "-m", msg):
        return

    # Push to GitHub
    if not run("git", "push", "origin", "master"):
        print("GitHub push failed, continuing with Vercel deploy...")

    print(f"Committed + pushed. Deploying to Vercel...")

    # Vercel --prod deploy
    r = subprocess.run(
        ["npx", "vercel", "--prod"],
        cwd=BLOG, capture_output=True, text=True, timeout=120
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