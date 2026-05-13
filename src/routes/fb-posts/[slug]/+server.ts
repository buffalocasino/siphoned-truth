import { error } from '@sveltejs/kit';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

export async function GET({ params }) {
  const { slug } = params;
  if (!slug) throw error(400, 'Missing slug');

  // Serverless functions on Vercel run from /var/task or similar.
  // Try known Vercel paths in order of likelihood.
  const candidates = [
    resolve('/var/task/static/fb-posts', `${slug}.txt`),
    resolve(process.cwd(), 'static/fb-posts', `${slug}.txt`),
    resolve(process.cwd(), '..', 'static/fb-posts', `${slug}.txt`),
    resolve(process.cwd(), '..', '..', 'static/fb-posts', `${slug}.txt`),
    resolve('/home/trevo/blog/static/fb-posts', `${slug}.txt`),
  ];

  let content = null;
  for (const p of candidates) {
    if (existsSync(p)) {
      content = readFileSync(p, 'utf-8');
      break;
    }
  }

  if (content === null) {
    throw error(404, `FB post not found: ${slug}`);
  }

  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}