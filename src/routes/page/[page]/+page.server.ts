import type { PageServerLoad } from './$types';

export const prerender = true;

const PAGE_SIZE = 20;

export async function entries() {
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });

	const articles: any[] = [];
	for (const [, mod] of Object.entries<any>(raw)) {
		if (!mod?.title) continue;
		const slug = mod.slug || mod.id || '';
		if (!slug) continue;
		articles.push(mod);
	}

	// Sort newest first
	articles.sort((a, b) => {
		const ta = new Date(a.time ?? 0).getTime();
		const tb = new Date(b.time ?? 0).getTime();
		return tb - ta;
	});

	const totalPages = Math.max(1, Math.ceil(articles.length / PAGE_SIZE));
	return Array.from({ length: totalPages }, (_, i) => ({ page: String(i + 1) }));
}

export const load: PageServerLoad = async ({ params }) => {
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });

	const articles: any[] = [];
	for (const [, mod] of Object.entries<any>(raw)) {
		if (!mod?.title) continue;
		const slug = mod.slug || mod.id || '';
		if (!slug) continue;
		articles.push(mod);
	}

	articles.sort((a, b) => {
		const ta = new Date(a.time ?? 0).getTime();
		const tb = new Date(b.time ?? 0).getTime();
		return tb - ta;
	});

	const page = Math.max(1, parseInt(params.page ?? '1', 10));
	const totalPages = Math.max(1, Math.ceil(articles.length / PAGE_SIZE));
	const safePage = Math.min(page, totalPages);
	const start = (safePage - 1) * PAGE_SIZE;
	const pageArticles = articles.slice(start, start + PAGE_SIZE);

	return {
		articles: pageArticles,
		page: safePage,
		totalPages,
		totalArticles: articles.length,
	};
};
