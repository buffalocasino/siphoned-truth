import type { PageServerLoad } from './$types';

export const prerender = true;

export const load: PageServerLoad = async () => {
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });
	const articles: any[] = [];

	for (const [path, mod] of Object.entries<any>(raw)) {
		const article = mod;
		if (!article?.title) continue;
		articles.push(article);
	}

	articles.sort((a: any, b: any) => {
		const ta = new Date(a?.time || a?.date || 0).getTime();
		const tb = new Date(b?.time || b?.date || 0).getTime();
		return tb - ta;
	});

	return { articles };
};