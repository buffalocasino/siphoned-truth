import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

// Vite glob import — bundles all JSON files at build time
const articleFiles = import.meta.glob('/src/lib/articles/*.json', { eager: true });

function safeTime(v: any): number {
	const t = v?.time || v?.date;
	if (!t) return 0;
	try { return new Date(t).getTime(); } catch { return 0; }
}

const articles = Object.values(articleFiles)
	.map((mod: any) => mod)
	.sort((a: any, b: any) => safeTime(b) - safeTime(a));

export const GET: RequestHandler = () => {
	return json({ articles });
};