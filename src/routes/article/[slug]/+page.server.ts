import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

// Vite glob import — bundles all JSON files at build time
const articleFiles = import.meta.glob('/src/lib/articles/*.json', { eager: true });

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;
	const fileKey = Object.keys(articleFiles).find(key =>
		key.toLowerCase().includes(slug.toLowerCase())
	);
	
	if (!fileKey) {
		throw error(404, 'Article not found');
	}

	const article = articleFiles[fileKey] as any;
	return { article };
};