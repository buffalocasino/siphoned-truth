import { json, error } from '@sveltejs/kit';
import { readFileSync } from 'fs';
import { join } from 'path';

export async function GET({ params }) {
  const { slug } = params;
  if (!slug) throw error(400, 'Missing slug');

  // Accept with or without .txt extension
  const filePath = join('static', 'fb-posts', `${slug}.txt`);
  try {
    const content = readFileSync(filePath, 'utf-8');
    return new Response(content, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'public, max-age=3600',
      },
    });
  } catch {
    throw error(404, `FB post not found: ${slug}`);
  }
}
