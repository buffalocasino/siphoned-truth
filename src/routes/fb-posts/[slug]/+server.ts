import { json, error } from '@sveltejs/kit';
import { readFileSync, existsSync } from 'fs';
import { resolve, join } from 'path';

export async function GET({ params }) {
  const { slug } = params;
  if (!slug) throw error(400, 'Missing slug');

  // Vercel serverless runs at /var/task
  const base = '/var/task';
  const candidates = [
    resolve(base, 'static', 'fb-posts', `${slug}.txt`),
    resolve(base, '..', 'static', 'fb-posts', `${slug}.txt`),
    resolve(base, '..', '..', 'static', 'fb-posts', `${slug}.txt`),
    resolve(process.cwd(), 'static', 'fb-posts', `${slug}.txt`),
  ];

  let content = null;
  let tried = [];
  for (const p of candidates) {
    tried.push(p + ' → ' + (existsSync(p) ? 'EXISTS' : 'MISSING'));
    if (existsSync(p)) {
      content = readFileSync(p, 'utf-8');
      break;
    }
  }

  if (content === null) {
    return json({ tried, cwd: process.cwd(), base });
  }

  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}