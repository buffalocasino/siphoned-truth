/**
 * Gazetteer of geopolitical and corporate hot-spots Siphoned Truth
 * investigations tend to cluster on. Lower-case keys are matched against
 * the article's `tags` array AND tokenized title words, so any article
 * touching e.g. "Iran" or "strait-of-hormuz" resolves to the same pin.
 *
 * Each entry: { lat, lon, region, zoom } — zoom is a sensible "fly-to" depth.
 * Multiple keys can map to one location (iran / irgc / tehran all → Tehran).
 */

export interface GazetteerEntry {
	lat: number;
	lon: number;
	region: string;
	zoom: number;
}

export const GAZETTEER: Record<string, GazetteerEntry> = {
	// --- Middle East ---
	'iran': { lat: 32.4279, lon: 53.688, region: 'Iran', zoom: 5 },
	'irgc': { lat: 32.4279, lon: 53.688, region: 'Iran', zoom: 5 },
	'tehran': { lat: 35.6892, lon: 51.389, region: 'Tehran, Iran', zoom: 9 },
	'strait-of-hormuz': { lat: 26.5667, lon: 56.25, region: 'Strait of Hormuz', zoom: 7 },
	'hormuz': { lat: 26.5667, lon: 56.25, region: 'Strait of Hormuz', zoom: 7 },
	'saudi': { lat: 23.8859, lon: 45.0792, region: 'Saudi Arabia', zoom: 5 },
	'riyadh': { lat: 24.7136, lon: 46.6753, region: 'Riyadh, Saudi Arabia', zoom: 9 },
	'uae': { lat: 23.4241, lon: 53.8478, region: 'UAE', zoom: 6 },
	'dubai': { lat: 25.2048, lon: 55.2708, region: 'Dubai, UAE', zoom: 9 },
	'israel': { lat: 31.0461, lon: 34.8516, region: 'Israel', zoom: 7 },
	'tel-aviv': { lat: 32.0853, lon: 34.7818, region: 'Tel Aviv, Israel', zoom: 10 },
	'gaza': { lat: 31.3547, lon: 34.3088, region: 'Gaza', zoom: 9 },
	'beirut': { lat: 33.8938, lon: 35.5018, region: 'Beirut, Lebanon', zoom: 10 },
	'lebanon': { lat: 33.8938, lon: 35.5018, region: 'Lebanon', zoom: 8 },
	'syria': { lat: 34.8021, lon: 38.9968, region: 'Syria', zoom: 6 },
	'damascus': { lat: 33.5138, lon: 36.2765, region: 'Damascus, Syria', zoom: 10 },
	'iraq': { lat: 33.2232, lon: 43.6793, region: 'Iraq', zoom: 5 },
	'baghdad': { lat: 33.3152, lon: 44.3661, region: 'Baghdad, Iraq', zoom: 10 },
	'yemen': { lat: 15.5527, lon: 48.5164, region: 'Yemen', zoom: 6 },

	// --- Russia / Eastern Europe ---
	'russia': { lat: 61.524, lon: 105.3188, region: 'Russia', zoom: 3 },
	'kremlin': { lat: 55.752, lon: 37.6175, region: 'Moscow, Russia', zoom: 10 },
	'moscow': { lat: 55.7558, lon: 37.6173, region: 'Moscow, Russia', zoom: 10 },
	'putin': { lat: 55.752, lon: 37.6175, region: 'Moscow, Russia', zoom: 10 },
	'ukraine': { lat: 48.3794, lon: 31.1656, region: 'Ukraine', zoom: 5 },
	'kyiv': { lat: 50.4501, lon: 30.5234, region: 'Kyiv, Ukraine', zoom: 10 },
	'crimea': { lat: 44.9521, lon: 34.1024, region: 'Crimea', zoom: 7 },
	'sevastopol': { lat: 44.6166, lon: 33.5254, region: 'Sevastopol, Crimea', zoom: 10 },
	'black-sea': { lat: 43.0, lon: 35.0, region: 'Black Sea', zoom: 5 },
	'belarus': { lat: 53.7098, lon: 27.9534, region: 'Belarus', zoom: 6 },

	// --- East / South Asia ---
	'china': { lat: 35.8617, lon: 104.1954, region: 'China', zoom: 3 },
	'beijing': { lat: 39.9042, lon: 116.4074, region: 'Beijing, China', zoom: 9 },
	'shanghai': { lat: 31.2304, lon: 121.4737, region: 'Shanghai, China', zoom: 9 },
	'xi-jinping': { lat: 39.9042, lon: 116.4074, region: 'Beijing, China', zoom: 9 },
	'hong-kong': { lat: 22.3193, lon: 114.1694, region: 'Hong Kong', zoom: 10 },
	'taiwan': { lat: 23.6978, lon: 120.9605, region: 'Taiwan', zoom: 7 },
	'taipei': { lat: 25.033, lon: 121.5654, region: 'Taipei, Taiwan', zoom: 10 },
	'japan': { lat: 36.2048, lon: 138.2529, region: 'Japan', zoom: 4 },
	'tokyo': { lat: 35.6762, lon: 139.6503, region: 'Tokyo, Japan', zoom: 10 },
	'north-korea': { lat: 40.3399, lon: 127.5101, region: 'North Korea', zoom: 6 },
	'pyongyang': { lat: 39.0392, lon: 125.7625, region: 'Pyongyang, N. Korea', zoom: 10 },
	'india': { lat: 20.5937, lon: 78.9629, region: 'India', zoom: 4 },
	'new-delhi': { lat: 28.6139, lon: 77.209, region: 'New Delhi, India', zoom: 9 },
	'mumbai': { lat: 19.076, lon: 72.8777, region: 'Mumbai, India', zoom: 10 },
	'pakistan': { lat: 30.3753, lon: 69.3451, region: 'Pakistan', zoom: 5 },

	// --- Americas ---
	'washington': { lat: 38.9072, lon: -77.0369, region: 'Washington, DC', zoom: 10 },
	'white-house': { lat: 38.8977, lon: -77.0365, region: 'White House, DC', zoom: 13 },
	'pentagon': { lat: 38.8719, lon: -77.0563, region: 'Pentagon, DC', zoom: 12 },
	'capitol': { lat: 38.8899, lon: -77.0091, region: 'US Capitol, DC', zoom: 12 },
	'trump': { lat: 38.8977, lon: -77.0365, region: 'Washington, DC', zoom: 10 },
	'new-york': { lat: 40.7128, lon: -74.006, region: 'New York, NY', zoom: 10 },
	'wall-street': { lat: 40.7069, lon: -74.0113, region: 'Wall Street, NY', zoom: 13 },
	'manhattan': { lat: 40.7831, lon: -73.9712, region: 'Manhattan, NY', zoom: 11 },
	'epstein': { lat: 25.8827, lon: -80.1242, region: 'Epstein properties, FL/NY', zoom: 9 },
	'epstein-island': { lat: 18.3398, lon: -64.9742, region: 'Little St. James, USVI', zoom: 12 },
	'little-st-james': { lat: 18.3398, lon: -64.9742, region: 'Little St. James, USVI', zoom: 12 },
	'national-mall': { lat: 38.8893, lon: -77.026, region: 'National Mall, DC', zoom: 13 },
	'los-angeles': { lat: 34.0522, lon: -118.2437, region: 'Los Angeles, CA', zoom: 10 },
	'san-francisco': { lat: 37.7749, lon: -122.4194, region: 'San Francisco, CA', zoom: 10 },
	'houston': { lat: 29.7604, lon: -95.3698, region: 'Houston, TX', zoom: 10 },
	'mexico': { lat: 23.6345, lon: -102.5528, region: 'Mexico', zoom: 4 },
	'mexico-city': { lat: 19.4326, lon: -99.1332, region: 'Mexico City', zoom: 10 },
	'cuba': { lat: 21.5218, lon: -77.7812, region: 'Cuba', zoom: 6 },
	'venezuela': { lat: 6.4238, lon: -66.5897, region: 'Venezuela', zoom: 5 },
	'caracas': { lat: 10.4806, lon: -66.9036, region: 'Caracas, Venezuela', zoom: 10 },
	'brazil': { lat: -14.235, lon: -51.9253, region: 'Brazil', zoom: 3 },

	// --- Europe ---
	'uk': { lat: 55.3781, lon: -3.436, region: 'United Kingdom', zoom: 5 },
	'britain': { lat: 55.3781, lon: -3.436, region: 'United Kingdom', zoom: 5 },
	'london': { lat: 51.5074, lon: -0.1278, region: 'London, UK', zoom: 10 },
	'paris': { lat: 48.8566, lon: 2.3522, region: 'Paris, France', zoom: 10 },
	'france': { lat: 46.6034, lon: 1.8883, region: 'France', zoom: 5 },
	'berlin': { lat: 52.52, lon: 13.405, region: 'Berlin, Germany', zoom: 10 },
	'germany': { lat: 51.1657, lon: 10.4515, region: 'Germany', zoom: 5 },
	'brussels': { lat: 50.8503, lon: 4.3517, region: 'Brussels, Belgium', zoom: 10 },
	'geneva': { lat: 46.2044, lon: 6.1432, region: 'Geneva, Switzerland', zoom: 10 },
	'davos': { lat: 46.8024, lon: 9.836, region: 'Davos, Switzerland', zoom: 11 },
	'wef': { lat: 46.8024, lon: 9.836, region: 'Davos, Switzerland', zoom: 11 },
	'zurich': { lat: 47.3769, lon: 8.5417, region: 'Zürich, Switzerland', zoom: 10 },
	'rome': { lat: 41.9028, lon: 12.4964, region: 'Rome, Italy', zoom: 10 },
	'italy': { lat: 41.8719, lon: 12.5674, region: 'Italy', zoom: 5 },
	'madrid': { lat: 40.4168, lon: -3.7038, region: 'Madrid, Spain', zoom: 10 },
	'spain': { lat: 40.4637, lon: -3.7492, region: 'Spain', zoom: 5 },
	'eu': { lat: 50.8503, lon: 4.3517, region: 'European Union', zoom: 4 },
	'european-union': { lat: 50.8503, lon: 4.3517, region: 'European Union', zoom: 4 },
	'nato': { lat: 50.8783, lon: 4.4196, region: 'NATO HQ, Brussels', zoom: 12 },

	// --- Africa ---
	'egypt': { lat: 26.8206, lon: 30.8025, region: 'Egypt', zoom: 5 },
	'cairo': { lat: 30.0444, lon: 31.2357, region: 'Cairo, Egypt', zoom: 10 },
	'sudan': { lat: 12.8628, lon: 30.2176, region: 'Sudan', zoom: 5 },
	'libya': { lat: 26.3351, lon: 17.2283, region: 'Libya', zoom: 5 },
	'nigeria': { lat: 9.082, lon: 8.6753, region: 'Nigeria', zoom: 5 },
	'south-africa': { lat: -30.5595, lon: 22.9375, region: 'South Africa', zoom: 4 },
	'congo': { lat: -4.0383, lon: 21.7587, region: 'DRC', zoom: 5 },
	'ethiopia': { lat: 9.145, lon: 40.4897, region: 'Ethiopia', zoom: 5 },

	// --- Institutions & corporate hot-spots ---
	'united-nations': { lat: 40.7489, lon: -73.968, region: 'UN HQ, New York', zoom: 13 },
	'imf': { lat: 38.8993, lon: -77.0469, region: 'IMF, Washington DC', zoom: 12 },
	'world-bank': { lat: 38.8993, lon: -77.0455, region: 'World Bank, DC', zoom: 12 },
	'goldman': { lat: 40.7069, lon: -74.0113, region: 'Goldman Sachs, NY', zoom: 13 },
	'jpmorgan': { lat: 40.7069, lon: -74.0113, region: 'JP Morgan, NY', zoom: 13 },
	'silicon-valley': { lat: 37.3875, lon: -122.0575, region: 'Silicon Valley, CA', zoom: 10 },
	'openai': { lat: 37.7749, lon: -122.4194, region: 'San Francisco, CA', zoom: 11 },
	'palo-alto': { lat: 37.4419, lon: -122.143, region: 'Palo Alto, CA', zoom: 12 },
	'blue-origin': { lat: 32.9904, lon: -106.975, region: 'Blue Origin, TX', zoom: 9 },
	'spacex': { lat: 33.9207, lon: -118.3278, region: 'SpaceX, Hawthorne CA', zoom: 11 },
	'florida': { lat: 27.6648, lon: -81.5158, region: 'Florida', zoom: 6 }
};

/**
 * Resolve an article to a geo pin.
 * Strategy:
 *  1. Explicit `coords: {lat, lon, region?}` on the article wins.
 *  2. Otherwise, look for any tag in the gazetteer (exact, lower-cased).
 *  3. Otherwise, tokenize the title and slug on non-alpha chars and
 *     look up each token of length ≥ 4.
 *  4. First match wins. If nothing matches, return null (article is dropped
 *     from the map — silent, not an error).
 */
export function resolveGeo(article: {
	coords?: { lat: number; lon: number; region?: string };
	tags?: string[];
	title?: string;
	slug?: string;
}): { lat: number; lon: number; region: string; zoom: number } | null {
	if (
		article.coords &&
		typeof article.coords.lat === 'number' &&
		typeof article.coords.lon === 'number'
	) {
		return {
			lat: article.coords.lat,
			lon: article.coords.lon,
			region: article.coords.region ?? 'Custom',
			zoom: 7
		};
	}

	const tags = (article.tags ?? []).map((t) => String(t).toLowerCase());
	for (const tag of tags) {
		if (GAZETTEER[tag]) return GAZETTEER[tag];
		// hyphenated tags: try each segment too (e.g. "strait-of-hormuz" → "strait", "of", "hormuz")
		for (const seg of tag.split('-')) {
			if (GAZETTEER[seg]) return GAZETTEER[seg];
		}
	}

	const title = (article.title ?? '').toLowerCase();
	const slug = (article.slug ?? '').toLowerCase();
	const haystack = `${title} ${slug}`;
	const tokens = haystack
		.split(/[^a-z0-9]+/)
		.filter((t) => t.length >= 4);

	// Prefer longer matches first to avoid "iran" matching when "iranian" was meant
	const sorted = [...new Set(tokens)].sort((a, b) => b.length - a.length);
	for (const token of sorted) {
		if (GAZETTEER[token]) return GAZETTEER[token];
	}

	return null;
}
