import type { Article } from '$lib/articles';
import { resolveGeo } from './gazetteer';
import type { MapPin } from './types';

/**
 * Convert the article corpus into mappable pins.
 * Articles that don't resolve to a location are dropped silently —
 * the map is opt-in by content, not exhaustive.
 */
export function buildPins(articles: Article[]): MapPin[] {
	const pins: MapPin[] = [];

	for (const a of articles) {
		if (!a.title || !a.slug) continue;
		const geo = resolveGeo(a);
		if (!geo) continue;

		const narrative = (a.narrative ?? a.article_body ?? a.content ?? a.summary ?? '').toString();
		const verdict = (a.verdict ?? '').toString();
		const telemetry = Array.isArray(a.telemetry)
			? a.telemetry
			: typeof a.telemetry === 'string'
				? a.telemetry.split('\n').filter(Boolean)
				: [];

		pins.push({
			slug: a.slug.toLowerCase(),
			id: a.id ?? a.slug,
			title: a.title,
			time: a.time ?? a.date ?? '',
			lat: geo.lat,
			lon: geo.lon,
			region: geo.region,
			preview: narrative.replace(/\s+/g, ' ').trim().slice(0, 160),
			verdict: verdict.replace(/\s+/g, ' ').trim().slice(0, 220),
			telemetryCount: telemetry.length
		});
	}

	// Newest first — matches the front-page feed order
	pins.sort((a, b) => {
		const ta = new Date(a.time || 0).getTime();
		const tb = new Date(b.time || 0).getTime();
		return tb - ta;
	});

	return pins;
}
