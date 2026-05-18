<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const article = $derived(data.article);
	const narrative = $derived((article.narrative ?? article.article_body ?? article.content ?? article.summary ?? '').toString());
	const getText = (field: string | undefined) => field ?? '';
</script>

<svelte:head>
	<title>{article.title} | The Siphoned Truth</title>
	<meta name="description" content={(narrative || '').slice(0, 160)} />
	<meta property="og:title" content={article.title || 'Article'} />
	<meta property="og:description" content={(narrative || '').slice(0, 200)} />
	<meta property="og:type" content="article" />
	<meta property="og:url" content={`https://siphonedtruth.online/article/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}`} />
	<meta property="og:image" content={`https://siphonedtruth.online/covers/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}.jpg`} />
	<meta property="og:image:width" content="1280" />
	<meta property="og:image:height" content="720" />
	<meta property="article:published_time" content={article.time} />
	<meta property="article:section" content={article.category || 'OSINT'} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={article.title} />
	<meta name="twitter:description" content={narrative.slice(0, 200)} />
	<meta name="twitter:image" content={`https://siphonedtruth.online/covers/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}.jpg`} />
	<link rel="canonical" href={`https://siphonedtruth.online/article/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}`} />
</svelte:head>

<main>
	<a href="/" class="back">← RETURN TO FEED</a>

	<article>
		<header>
			<div class="classification">⬡ SHADOW BROKER INTEGRATION NODE</div>
			<h1>[ENCRYPTED REPORT: SIPHONED TRUTH]</h1>
			<div class="meta">
				<span>ID: {article.id}</span>
				<span>•</span>
				<span>TIME: {article.time}</span>
			</div>
		</header>

		<div class="cover-image">
			<img src="/covers/{article.slug?.toLowerCase() ?? article.id.toLowerCase()}.jpg" alt={article.title} />
		</div>

<section class="section">
		<h2>I. PUBLIC NARRATIVE</h2>
		<p>{narrative}</p>
	</section>

	<section class="section telemetry">
		<h2>II. TELEMETRY FEED</h2>
		<ul>
			{#each (article.telemetry ?? []) as item}
				<li>{item}</li>
			{/each}
		</ul>
	</section>

	<section class="section">
		<h2>III. ADVERSARIAL ANALYSIS</h2>
		<p>{getText(article.analysis)}</p>
	</section>

	<section class="section verdict">
		<h2>IV. THE VERDICT</h2>
		<blockquote>{getText(article.verdict)}</blockquote>
	</section>

		<section class="section sources">
			<h2>V. SOURCE TELEMETRY</h2>
			<p>Data cross-referenced from: AIS ship tracking (MarineTraffic/OpenSeaMap), OpenSky Network flight telemetry, NASA FIRMS fire hotspot data, EIA energy stock reports, EIA petroleum status reports, Reuters/House Reuters energy coverage, Platts commodity benchmarks, State Department press briefings, CENTCOM public statements, and public aviation databases.</p>
			<div class="source-note">
				<span>FEED STATUS: VERIFIED</span>
				<span>•</span>
				<span>AUTH: HERMES_AGENT_V4</span>
				<span>•</span>
				<span>CROSS-REFERENCED: {(article.telemetry ?? []).length} DATA POINTS</span>
			</div>
		</section>

		<div class="ad-slot">
		<ins class="adsbygoogle"
			 style="display:block; width:300px; height:250px; margin:0 auto;"
			 data-ad-client="ca-pub-1032028091690286"
			 data-ad-slot="auto"
			 data-ad-format="auto"
			 data-full-width-responsive="true"></ins>
	</div>

		<footer>
			<span>AUTH: HERMES_AGENT_V4</span>
			<span>•</span>
			<span>SIG: SHADOW_NODE_01</span>
			<span>•</span>
			<span>SEC_LEVEL: UNRESTRICTED_PUBLIC</span>
		</footer>
	</article>
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
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
	}

	.back {
		display: inline-block;
		color: #00ff8877;
		text-decoration: none;
		font-size: 0.7rem;
		letter-spacing: 0.2em;
		margin-bottom: 2rem;
	}

	.back:hover { color: #00ff88; }

	article {
		background: #0f0f18;
		border: 1px solid #00ff8822;
		padding: 2.5rem;
	}

	header {
		text-align: center;
		margin-bottom: 2.5rem;
		padding-bottom: 1.5rem;
		border-bottom: 1px solid #00ff8822;
	}

	.classification {
		font-size: 0.6rem;
		color: #00ff8866;
		letter-spacing: 0.3em;
		margin-bottom: 1rem;
	}

	h1 {
		font-size: 1.1rem;
		font-weight: 400;
		color: #00ff88;
		letter-spacing: 0.15em;
		margin: 0 0 1rem;
	}

	.meta {
		font-size: 0.65rem;
		color: #00ff8855;
		letter-spacing: 0.15em;
		display: flex;
		gap: 0.75rem;
		justify-content: center;
	}

	.cover-image {
		width: 100%;
		max-height: 400px;
		overflow: hidden;
		margin-bottom: 2rem;
		border: 1px solid #00ff8822;
	}

	.cover-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.section {
		margin-bottom: 2rem;
	}

	.section h2 {
		font-size: 0.75rem;
		color: #00ff88;
		letter-spacing: 0.25em;
		font-weight: 400;
		margin: 0 0 1.2rem;
		padding-bottom: 0.5rem;
		border-bottom: 1px solid #00ff8811;
	}

	.section p {
		font-size: 1rem;
		color: #00ff88cc;
		line-height: 1.9;
		margin: 0;
	}

	.telemetry ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	.telemetry li {
		font-size: 0.875rem;
		color: #00ff8899;
		line-height: 1.7;
		padding: 0.4rem 0;
		border-bottom: 1px solid #00ff8811;
	}

	.telemetry li::before {
		content: '◆ ';
		color: #00ff8855;
	}

	.verdict blockquote {
		border-left: 3px solid #ff4444;
		padding-left: 1.5rem;
		margin: 0;
	}

	.verdict p {
		font-size: 1.05rem;
		color: #ff4444;
		font-weight: 400;
	}

	footer {
		margin-top: 2.5rem;
		padding-top: 1.5rem;
		border-top: 1px solid #00ff8822;
		display: flex;
		gap: 1rem;
		justify-content: center;
		font-size: 0.6rem;
		color: #00ff8833;
		letter-spacing: 0.15em;
	}

	.sources {
		border-top: 1px dashed #00ff8833;
		padding-top: 1.5rem;
	}

	.sources p {
		font-size: 0.825rem;
		color: #00ff8866;
		line-height: 1.7;
	}

	.source-note {
		margin-top: 0.75rem;
		font-size: 0.6rem;
		color: #00ff8844;
		letter-spacing: 0.12em;
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
	}

	.ad-slot {
		border: 1px dashed #ffffff22;
		color: #ffffff22;
		font-size: 0.65rem;
		letter-spacing: 0.2em;
		text-align: center;
		padding: 1.5rem;
		margin: 1.5rem 0;
		width: 300px;
		max-width: 100%;
	}
</style>