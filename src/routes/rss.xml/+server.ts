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
		narrative?: string;
		verdict?: string;
		tags?: string[];
	}

	const articles: Article[] = [];
	for (const [, mod] of Object.entries<Article>(raw)) {
		const slug = ((mod.slug || mod.id || '').toLowerCase());
		if (!mod?.title || !slug) continue;
		articles.push(mod);
	}

	// Sort newest first, limit to 50 most recent
	articles.sort((a, b) => {
		const ta = new Date(a.time ?? 0).getTime();
		const tb = new Date(b.time ?? 0).getTime();
		return tb - ta;
	});
	const recent = articles.slice(0, 50);

	const BASE = 'https://siphonedtruth.online';
	const now = new Date().toUTCString();
	const siteTitle = 'The Siphoned Truth';
	const siteDesc = 'Adversarial OSINT Intelligence Bureau — cross-referencing elite deception via raw telemetry since 2025';

	const items = recent.map((a) => {
		const slug = (a.slug || a.id || '').toLowerCase();
		const url = `${BASE}/article/${encodeURIComponent(slug)}`;
		const pubDate = a.time ? new Date(a.time).toUTCString() : now;
		const narrative = (a.narrative || '').replace(/<[^>]+>/g, '').slice(0, 300).trim();
		const title = (a.title || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		const desc = narrative.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		const category = a.category || 'OSINT';
		return `  <item>
    <title>${title}</title>
    <link>${url}</link>
    <guid isPermaLink="true">${url}</guid>
    <pubDate>${pubDate}</pubDate>
    <category>${category}</category>
    <description>${desc}${desc.length >= 300 ? '...' : ''}</description>
  </item>`;
	}).join('\n');

	const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>${siteTitle}</title>
    <link>${BASE}</link>
    <description>${siteDesc}</description>
    <language>en-us</language>
    <lastBuildDate>${now}</lastBuildDate>
    <atom:link href="${BASE}/rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>${BASE}/og-default.jpg</url>
      <title>${siteTitle}</title>
      <link>${BASE}</link>
    </image>
${items}
  </channel>
</rss>`;

	return new Response(xml, {
		headers: {
			'Content-Type': 'application/rss+xml; charset=utf-8',
			'Cache-Control': 'max-age=1800',
		},
	});
};
