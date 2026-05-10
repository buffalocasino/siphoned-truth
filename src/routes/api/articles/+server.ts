import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

// Vite glob import — bundles all JSON files at build time
const articleFiles = import.meta.glob('/src/lib/articles/*.json', { eager: true });

const articles = Object.values(articleFiles).map((mod: any) => {
	// Keep all fields: narrative, telemetry, analysis, verdict
	return mod;
}).sort((a: any, b: any) => new Date(b.time).getTime() - new Date(a.time).getTime());

export const GET: RequestHandler = () => {
	return json({ articles });
};