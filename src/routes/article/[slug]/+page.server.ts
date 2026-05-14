import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';
import { readdir } from 'fs/promises';
import { join } from 'path';

export const load: PageServerLoad = async ({ params }) => {
	const { slug } = params;
	const normalizedSlug = slug.toLowerCase();

	const articlesDir = join(process.cwd(), 'src/lib/articles');
	let files: string[];

	try {
		files = await readdir(articlesDir);
	} catch {
		throw error(404, 'Article not found');
	}

	for (const file of files) {
		if (!file.endsWith('.json')) continue;
		const filePath = join(articlesDir, file);
		try {
			const { readFile } = await import('fs/promises');
			const content = await readFile(filePath, 'utf-8');
			const article = JSON.parse(content);
			const articleSlug = (article.slug || article.id || '').toLowerCase();
			if (articleSlug === normalizedSlug || file.replace('.json', '').toLowerCase() === normalizedSlug) {
				if (!article.title) throw error(404, 'Article not found');
				return { article };
			}
		} catch (e) {
			if ((e as any)?.status === 404) throw e;
		}
	}

	throw error(404, 'Article not found');
};