import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const prerender = true;

export async function entries() {
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });
	const slugs: string[] = [];

	for (const [path, mod] of Object.entries<any>(raw)) {
		const article = mod;
		if (!article?.title) continue;
		const slug = (article.slug || article.id || path.replace('/src/lib/articles/', '').replace('.json', '')).toLowerCase();
		slugs.push(slug);
	}

	return slugs.map(slug => ({ slug }));
}

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;
	const normalizedSlug = slug.toLowerCase();

	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });

	for (const [path, mod] of Object.entries<any>(raw)) {
		const article = mod;
		if (!article?.title) continue;
		const articleSlug = (article.slug || article.id || path.replace('/src/lib/articles/', '').replace('.json', '')).toLowerCase();
		if (articleSlug === normalizedSlug) {
			return { article };
		}
	}

	throw error(404, 'Article not found');
};