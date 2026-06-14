import type { PageServerLoad } from './$types';
import { buildPins } from '$lib/map/loader';

export const prerender = true;

export const load: PageServerLoad = async () => {
	// Same glob the front page uses — keeps article source identical
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });
	const articles: any[] = [];
	for (const [, mod] of Object.entries<any>(raw)) {
		if (mod?.title) articles.push(mod);
	}

	const pins = buildPins(articles);

	return {
		pins,
		stats: {
			totalArticles: articles.length,
			mappedArticles: pins.length,
			regions: new Set(pins.map((p) => p.region)).size
		}
	};
};
