import type { PageServerLoad } from './$types';

const articleFiles = import.meta.glob('/src/lib/articles/*.json', { eager: true });

function safeTime(v: any): number {
	const t = v?.time || v?.date;
	if (!t) return 0;
	try { return new Date(t).getTime(); } catch { return 0; }
}

export const load: PageServerLoad = () => {
	try {
		const raw = Object.values(articleFiles);
		const articles = raw
			.map((mod: any) => mod?.default ?? mod)
			.sort((a: any, b: any) => safeTime(b) - safeTime(a));
		return { articles };
	} catch (e) {
		console.error('Article load error:', e);
		return { articles: [] };
	}
};