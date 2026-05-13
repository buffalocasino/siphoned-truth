import { json, error } from '@sveltejs/kit';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

export async function GET({ params }) {
  const { slug } = params;
  if (!slug) throw error(400, 'Missing slug');

  const base = process.cwd();
  const filePath = join(base, 'static', 'fb-posts', `${slug}.txt`);
  if (!existsSync(filePath)) {
    throw error(404, `FB post not found: ${slug}`);
  }
  const content = readFileSync(filePath, 'utf-8');
  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
