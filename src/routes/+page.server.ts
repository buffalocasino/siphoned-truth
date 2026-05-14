import type { PageServerLoad } from './$types';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

function safeTime(v: any): number {
	const t = v?.time || v?.date;
	if (!t) return 0;
	try { return new Date(t).getTime(); } catch { return 0; }
}

export const load: PageServerLoad = async () => {
	const articlesDir = join(process.cwd(), 'src/lib/articles');
	let files: string[] = [];

	try {
		files = await readdir(articlesDir);
	} catch {
		return { articles: [] };
	}

	const articles = [];
	for (const file of files) {
		if (!file.endsWith('.json')) continue;
		try {
			const content = await readFile(join(articlesDir, file), 'utf-8');
			const article = JSON.parse(content);
			if (article && article.title) {
				articles.push(article);
			}
		} catch { /* skip bad files */ }
	}

	articles.sort((a: any, b: any) => safeTime(b) - safeTime(a));
	return { articles };
};