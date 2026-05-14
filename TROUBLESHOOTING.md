# Siphoned Truth — Deployment Troubleshooting

## The Problem
Vercel deploys fail with `"No Output Files detected"` or serverless function size errors.

**Root cause:** The project uses SvelteKit's SSR prerendering (`prerender = true` on all routes). Every article page is a static HTML file in `.vercel/output/static/`. The `npm run build` output is a full static site — there is no serverless function to run. Vercel's default build detection sees no server output and throws an error.

**Why it worked before (sometimes):** Older versions of the project may have had `output: 'static'` set in `svelte.config.js`, which tells Vercel to expect static output. Without it, Vercel runs `npm run build` on their servers and expects a deployment artifact.

---

## The Fix
Always use `--prebuilt`:

```bash
# WRONG — hits serverless detection and fails
npx vercel --prod --force

# RIGHT — uploads the already-built static output
npx vercel --prod --prebuilt --yes
```

The `--prebuilt` flag tells Vercel: "use the `.vercel/output` directory that already exists from a local build." It skips server-side build entirely.

---

## auto_deploy.py deploy step
The script now runs `npm run build` locally first, then uses `--prebuilt`:

```
1. npm run build          ← local, builds to .vercel/output/
2. git push origin master
3. npx vercel --prod --prebuilt --yes   ← uploads pre-built output
```

---

## If --prebuilt still fails

### "No Output Files detected"
The `.vercel/output` directory is missing or empty. Check:
```bash
ls .vercel/output/static/  # should contain index.html, article/, etc.
```

If empty, the local build failed:
```bash
npm run build  # run manually to see the error
```

### "Build Mounting Error"
The `.vercel/output` was created with a different Node version. Clear and rebuild:
```bash
rm -rf .vercel/output
npm run build
npx vercel --prod --prebuilt --yes
```

### Serverless function size errors (H10, KError)
Someone added a server-side route (API route, non-prerendered page). The project is supposed to be fully static. Check `svelte.config.js`:

```js
// WRONG — enables SSR
export default {
  kit: {
    adapter: adapter-auto
  }
}

// RIGHT — forces static output for ALL routes
export default {
  kit: {
    adapter: adapter-static  // or adapter-vercel with prerender: true
  }
}
```

If you need an API route, move it to a separate service.

---

## Verdict validation failures
Articles with missing or improperly prefixed verdicts are flagged but not excluded. Fix before deploy:

```
MISSING VERDICT: some-article.json
MISSING PREFIX: another-article.json — verdict: "This happened..."
```

Verdict must start with `[SIPHONED VERDICT]` (with colon).

---

## Cover images
MiniMax image generation tracks processed slugs in `.deployed_slugs`. To re-generate a specific cover:
```bash
# Remove from processed list and delete the image
sed -i '/^slug-name$/d' .deployed_slugs
rm static/covers/slug-name.jpg
python auto_deploy.py  # will regenerate on next run
```

---

## Useful commands
```bash
cd ~/blog

# Dry run (syncs + validates, no deploy)
python auto_deploy.py

# Manual deploy
npm run build && npx vercel --prod --prebuilt --yes

# Check what Vercel project this is linked to
npx vercel link 2>&1 | head -5

# Force a fresh build on Vercel (rarely needed now)
npx vercel --prod --force --yes  # will likely fail — use --prebuilt
```