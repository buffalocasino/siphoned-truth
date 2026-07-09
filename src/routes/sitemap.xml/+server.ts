import type { RequestHandler } from './$types';

export const prerender = true;

export const GET: RequestHandler = async () => {
	const raw = import.meta.glob('/src/lib/articles/*.json', { eager: true, import: 'default' });

	interface Article {
		slug?: string;
		id?: string;
		title?: string;
		time?: string;
		category?: string;
	}

	const articles: Article[] = [];
	for (const [, mod] of Object.entries<Article>(raw)) {
		const slug = ((mod.slug || mod.id || '').toLowerCase());
		if (!mod?.title || !slug) continue;
		articles.push(mod);
	}

	// Sort newest first
	articles.sort((a, b) => {
		const ta = new Date(a.time ?? 0).getTime();
		const tb = new Date(b.time ?? 0).getTime();
		return tb - ta;
	});

	const BASE = 'https://siphonedtruth.online';
	const today = new Date().toISOString().split('T')[0];

	const urls = articles.map((a) => {
		const slug = (a.slug || a.id || '').toLowerCase();
		const lastmod = a.time ? new Date(a.time).toISOString().split('T')[0] : today;
		return `  <url>
    <loc>${BASE}/article/${encodeURIComponent(slug)}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>`;
	}).join('\n');

	const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${BASE}/</loc>
    <changefreq>hourly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${BASE}/map</loc>
    <changefreq>daily</changefreq>
    <priority>0.6</priority>
  </url>
${urls}
</urlset>`;

	return new Response(xml, {
		headers: {
			'Content-Type': 'application/xml',
			'Cache-Control': 'max-age=3600',
		},
	});
};
