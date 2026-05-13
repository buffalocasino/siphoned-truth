import { error } from '@sveltejs/kit';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

export async function GET({ params }) {
  const { slug } = params;
  if (!slug) throw error(400, 'Missing slug');

  // Vercel serverless functions run from /var/task — resolve project root
  // via the VERCEL environment variable, falling back to cwd
  const isVercel = !!process.env.VERCEL;
  const base = isVercel
    ? join(process.env.VERCEL_PROJECT_ROOT_PATH ?? process.cwd())
    : process.cwd();

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
