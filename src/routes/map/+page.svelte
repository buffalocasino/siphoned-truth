<script lang="ts">
	import MapView from '$lib/map/MapView.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const pins = $derived(data.pins);
	const stats = $derived(data.stats);

	// Group pins by region for the sidebar list (newest first inside each region)
	const regions = $derived(() => {
		const map = new Map<string, typeof pins>();
		for (const p of pins) {
			if (!map.has(p.region)) map.set(p.region, []);
			map.get(p.region)!.push(p);
		}
		return [...map.entries()]
			.map(([region, items]) => ({ region, count: items.length, latest: items[0] }))
			.sort((a, b) => b.count - a.count);
	});
</script>

<svelte:head>
	<title>Investigation Heatmap | The Siphoned Truth</title>
	<meta
		name="description"
		content="Geographic distribution of Siphoned Truth investigations. Click any pin to read the dossier."
	/>
	<meta property="og:title" content="Investigation Heatmap | The Siphoned Truth" />
	<meta
		property="og:description"
		content="Geographic distribution of Siphoned Truth investigations."
	/>
	<link rel="canonical" href="https://siphonedtruth.online/map" />
</svelte:head>

<main>
	<nav class="topnav">
		<a href="/" class="back">← RETURN TO FEED</a>
		<div class="classification">⬡ GEOSPATIAL THREAT MATRIX</div>
	</nav>

	<section class="intro">
		<h1>[GLOBAL HEATMAP // {stats.mappedArticles} ACTIVE DOSSIERS]</h1>
		<p class="lede">
			{stats.mappedArticles} of {stats.totalArticles} investigations mapped across {stats.regions}
			distinct regions. Hover for dossier preview. Click to open.
		</p>
	</section>

	<section class="map-section">
		<MapView {pins} />
	</section>

	<section class="region-index">
		<h2>REGION INDEX</h2>
		<div class="region-grid">
			{#each regions() as r}
				<a class="region-card" href={`/article/${r.latest.slug}`}>
					<div class="region-name">▸ {r.region}</div>
					<div class="region-count">{r.count} DOSSIER{r.count === 1 ? '' : 'S'}</div>
					<div class="region-latest">{r.latest.title}</div>
				</a>
			{/each}
		</div>
	</section>

	<footer>
		<span>SIG: SHADOW_NODE_01</span>
		<span>•</span>
		<span>BASEMAP: CARTO DARK_MATTER (OSM)</span>
		<span>•</span>
		<span>RESOLVER: TAG/TOKEN GAZETTEER v1</span>
		<span>•</span>
		<a href="https://deflock.org" target="_blank" rel="noopener" class="footer-link">▸ DEFLOCK.ORG / FLOCK CAM</a>
	</footer>
</main>

<style>
	:global(body) {
		background: #0a0a0f;
		color: #00ff88;
		font-family: 'Courier New', monospace;
		margin: 0;
		min-height: 100vh;
	}

	main {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem 1.5rem 4rem;
	}

	.topnav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
		padding-bottom: 0.75rem;
		border-bottom: 1px solid #00ff8822;
	}

	.back {
		color: #00ff8877;
		text-decoration: none;
		font-size: 0.7rem;
		letter-spacing: 0.2em;
		transition: color 0.2s;
	}

	.back:hover {
		color: #00ff88;
	}

	.classification {
		font-size: 0.6rem;
		color: #00ff8866;
		letter-spacing: 0.3em;
	}

	.intro {
		margin-bottom: 1.5rem;
		text-align: center;
	}

	h1 {
		font-size: 1rem;
		font-weight: 400;
		letter-spacing: 0.25em;
		color: #00ff88;
		margin: 0 0 0.75rem;
		text-shadow: 0 0 20px #00ff8844;
	}

	.lede {
		font-size: 0.75rem;
		color: #00ff88aa;
		letter-spacing: 0.12em;
		margin: 0;
		line-height: 1.7;
	}

	h2 {
		font-size: 0.75rem;
		font-weight: 400;
		letter-spacing: 0.3em;
		color: #00ff88;
		margin: 0 0 1rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid #00ff8822;
	}

	.map-section {
		margin-bottom: 2.5rem;
	}

	.region-index {
		margin-bottom: 2rem;
	}

	.region-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
		gap: 0.75rem;
	}

	.region-card {
		background: #0f0f18;
		border: 1px solid #00ff8822;
		padding: 0.9rem 1rem;
		text-decoration: none;
		color: inherit;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		transition: border-color 0.2s, box-shadow 0.2s;
	}

	.region-card:hover {
		border-color: #00ff8855;
		box-shadow: 0 0 16px #00ff8811;
	}

	.region-name {
		font-size: 0.7rem;
		color: #00ff88;
		letter-spacing: 0.2em;
	}

	.region-count {
		font-size: 0.6rem;
		color: #00ff8855;
		letter-spacing: 0.2em;
	}

	.region-latest {
		font-size: 0.7rem;
		color: #00ff88aa;
		line-height: 1.5;
		margin-top: 0.25rem;
	}

	footer {
		margin-top: 3rem;
		padding-top: 1.5rem;
		border-top: 1px solid #00ff8822;
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
		font-size: 0.6rem;
		color: #00ff8833;
		letter-spacing: 0.15em;
	}

	.footer-link {
		color: #00ff8877;
		text-decoration: none;
		transition: color 0.2s;
	}

	.footer-link:hover {
		color: #00ff88;
	}
</style>
