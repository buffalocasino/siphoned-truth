import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ fetch: fetchFn }) => {
	try {
		const res = await fetchFn('/articles/');
		if (!res.ok) return { articles: [] };

		// Vercel serverless can use fs for static files in the deployment
		const { readFileSync, readdirSync } = await import('fs');
		const { join } = await import('path');
		const articlesDir = join(process.cwd(), 'static', 'articles');
		const files = readdirSync(articlesDir).filter(f => f.endsWith('.json'));
		const articles: any[] = [];

		for (const file of files) {
			try {
				const content = readFileSync(join(articlesDir, file), 'utf-8');
				const article = JSON.parse(content);
				if (article?.title) articles.push(article);
			} catch { /* skip bad files */ }
		}

		articles.sort((a: any, b: any) => {
			const ta = new Date(a?.time || a?.date || 0).getTime();
			const tb = new Date(b?.time || b?.date || 0).getTime();
			return tb - ta;
		});

		return { articles };
	} catch {
		return { articles: [] };
	}
};