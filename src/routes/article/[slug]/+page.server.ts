import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

// Vite glob import — bundles all JSON files at build time
const articleFiles = import.meta.glob('/src/lib/articles/*.json', { eager: true });

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;
	const normalizedSlug = slug.toLowerCase();

	// Find by slug field OR by filename match (handles slug ≠ filename)
	const fileKey = Object.keys(articleFiles).find(key => {
		const keyLower = key.toLowerCase();
		const mod = (articleFiles[key] as any);
		const article = mod?.default ?? mod;
		// Match by slug field first
		if (article?.slug?.toLowerCase() === normalizedSlug) return true;
		// Fallback: filename contains the slug segments
		const fileBase = keyLower.replace('/src/lib/articles/', '').replace('.json', '');
		return fileBase.includes(normalizedSlug) || normalizedSlug.includes(fileBase);
	});

	if (!fileKey) {
		throw error(404, 'Article not found');
	}

	const raw = articleFiles[fileKey] as any;
	const article = raw?.default ?? raw;
	if (!article || !article.title) {
		throw error(404, 'Article not found');
	}
	return { article };
};