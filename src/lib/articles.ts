export interface Article {
	slug: string;
	id?: string;
	time?: string;
	date?: string;
	title: string;
	narrative?: string;
	article_body?: string;
	content?: string;
	summary?: string;
	telemetry?: string[];
	analysis?: string;
	verdict?: string;
	coverImage?: string;
	coverPrompt?: string;
}

export function getAllArticles(): Article[] {
	if (typeof window !== 'undefined') return [];

	try {
		const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });
		const articles: Article[] = [];
		for (const [, mod] of Object.entries<any>(raw)) {
			if (mod?.title) articles.push(mod as Article);
		}
		return articles;
	} catch {
		return [];
	}
}

export function getArticle(slug: string): Article | undefined {
	if (typeof window !== 'undefined') return undefined;

	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });
	const normalizedSlug = slug.toLowerCase();

	for (const [path, mod] of Object.entries<any>(raw)) {
		const article = mod as Article;
		if (!article?.title) continue;
		const articleSlug = (article.slug || article.id || path.replace('/src/lib/articles/', '').replace('.json', '')).toLowerCase();
		if (articleSlug === normalizedSlug) return article;
	}
	return undefined;
}

export function safeTime(v: Article): number {
	const t = v?.time || v?.date;
	if (!t) return 0;
	try { return new Date(t).getTime(); } catch { return 0; }
}