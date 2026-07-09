<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const article = $derived(data.article);
	const narrative = $derived((article.narrative ?? article.article_body ?? article.content ?? article.summary ?? '').toString());
	const getText = (field: string | undefined) => field ?? '';
	const telemetryItems = $derived(
		Array.isArray(article.telemetry)
			? article.telemetry
			: typeof article.telemetry === 'string'
				? article.telemetry.split('\n').filter(Boolean)
				: []
	);

	const shareUrl = $derived(`https://siphonedtruth.online/article/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}`);
	const shareTitle = $derived(encodeURIComponent(article.title ?? ''));

	const parseContent = (text: string) => {
		const lines = text.split('\n');
		const parts: string[] = [];
		let inList = false;
		for (const line of lines) {
			if (line.startsWith('## ')) {
				if (inList) { parts.push('</ul>'); inList = false; }
				parts.push(`<h3 class="content-heading">${line.slice(3)}</h3>`);
			} else if (line.startsWith('- ')) {
				if (!inList) { parts.push('<ul class="content-list">'); inList = true; }
				parts.push(`<li>${line.slice(2)}</li>`);
			} else if (line.startsWith('**')) {
				// Bold intro lines like **KEY CLAIM:** treated as sub-headings
				if (inList) { parts.push('</ul>'); inList = false; }
				const match = line.match(/^\*\*(.+?)\*\*[:\s]*(.*)$/);
				if (match) {
					parts.push(`<p class="content-strong"><strong>${match[1]}:</strong> ${match[2]}</p>`);
				} else {
					parts.push(`<p>${line}</p>`);
				}
			} else if (line.trim()) {
				if (inList) { parts.push('</ul>'); inList = false; }
				parts.push(`<p>${line}</p>`);
			}
		}
		if (inList) parts.push('</ul>');
		return parts.join('\n');
	};
</script>

<svelte:head>
	<title>{article.title} | The Siphoned Truth</title>
	<meta name="description" content={(narrative || '').slice(0, 160)} />
	<meta property="og:title" content={article.title || 'Article'} />
	<meta property="og:description" content={(narrative || '').slice(0, 200)} />
	<meta property="og:type" content="article" />
	<meta property="og:url" content={`https://siphonedtruth.online/article/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}`} />
	<meta property="og:image" content={article.coverImage || `https://siphonedtruth.online/covers/${(article.slug?.toLowerCase() ?? article.id.toLowerCase())}.jpg`} />
	<meta property="og:image:width" content="1280" />
	<meta property="og:image:height" content="720" />
	<meta property="article:published_time" content={article.time} />
	<meta property="article:section" content={article.category || 'OSINT'} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={article.title} />
	<meta name="twitter:description" content={narrative.slice(0, 200)} />
	<meta name="twitter:image" content={article.coverImage || `https://siphonedtruth.online/covers/${(article.slug?.toLowerCase() ?? article.id.toLowerCase())}.jpg`} />
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
				<img src={article.coverImage || `/covers/${(article.slug?.toLowerCase() ?? article.id.toLowerCase())}.jpg`} alt={article.title} />
			</div>

	<section class="section">
		<h2>I. PUBLIC NARRATIVE</h2>
		<div class="narrative-text">
		  {@html parseContent(narrative)}
		</div>
	</section>

	<section class="section telemetry">
		<h2>II. TELEMETRY FEED</h2>
		<ul>
			{#each telemetryItems as item}
				<li>{item}</li>
			{/each}
		</ul>
	</section>

	<section class="section">
		<h2>III. ADVERSARIAL ANALYSIS</h2>
		<div class="analysis-text">
		  {@html parseContent(getText(article.analysis))}
		</div>
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
				<span>CROSS-REFERENCED: {telemetryItems.length} DATA POINTS</span>
			</div>
		</section>

		<div class="share-bar">
			<span class="share-label">SHARE</span>
			<a href="https://twitter.com/intent/tweet?url={shareUrl}&text={shareTitle}&via=_Norvell_" target="_blank" rel="noopener" class="share-btn twitter" aria-label="Share on X">
				<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
			</a>
			<a href="https://www.facebook.com/sharer/sharer.php?u={shareUrl}" target="_blank" rel="noopener" class="share-btn facebook" aria-label="Share on Facebook">
				<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
			</a>
			<a href="https://www.reddit.com/submit?url={shareUrl}&title={shareTitle}" target="_blank" rel="noopener" class="share-btn reddit" aria-label="Share on Reddit">
				<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm6.5 13.5a1.5 1.5 0 0 1-2.55 1.05 7.5 7.5 0 0 1-4.1 1.2l.7 3.3 2.3-.5a1.2 1.2 0 1 1 .1.6l-2.6.5a.4.4 0 0 1-.4-.2l-.8-3.7a7.5 7.5 0 0 1-4.3-1.2 1.5 1.5 0 1 1-1.65-2.4 4.5 4.5 0 0 1 .1-1.9c-.9-.4-2.1-1.5-1.9-3 .2-1.5 1.4-2.4 2.4-2.4.7 0 1.4.3 1.8.8a8.5 8.5 0 0 1 4.6 0 2.5 2.5 0 0 1 1.8-.8c1 0 2.2.9 2.4 2.4.2 1.5-1 2.6-1.9 3a4.5 4.5 0 0 1 .1 1.9 1.5 1.5 0 0 1 .9 2.4zm-10-3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm7 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/></svg>
			</a>
			<button class="share-btn copy" onclick={async () => { await navigator.clipboard.writeText(shareUrl); }} aria-label="Copy link">
				<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
			</button>
		</div>

		<div class="ad-slot">
		<ins class="adsbygoogle"
			 style="display:block; width:300px; height:250px; margin:0 auto;"
			 data-ad-client="ca-pub-1032028091690286"
			 	data-ad-format="auto"
			 	data-full-width-responsive="true"></ins>
	</div>

		<footer>
			<span>AUTH: HERMES_AGENT_V4</span>
			<span>•</span>
			<span>SIG: SHADOW_NODE_01</span>
			<span>•</span>
			<span>SEC_LEVEL: UNRESTRICTED_PUBLIC</span>
			<span>•</span>
			<a href="/map" class="footer-link">▸ HEATMAP</a>
			<span>•</span>
			<a href="https://deflock.org" target="_blank" rel="noopener" class="footer-link">▸ DEFLOCK.ORG</a>
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

	.narrative-text :global(p),
	.analysis-text :global(p),
	.narrative-text :global(.content-strong),
	.analysis-text :global(.content-strong) {
		font-size: 1rem;
		color: #00ff88cc;
		line-height: 1.9;
		margin: 0 0 1.2rem;
	}

	.content-heading {
		font-size: 0.85rem;
		color: #00ff88;
		letter-spacing: 0.2em;
		font-weight: 400;
		margin: 2rem 0 0.75rem;
		text-transform: uppercase;
	}

	.content-strong strong {
		color: #00ff88;
	}

	:global(.content-list) {
		list-style: none;
		padding: 0;
		margin: 0 0 1.5rem;
	}

	:global(.content-list li) {
		font-size: 0.9rem;
		color: #00ff88cc;
		line-height: 1.7;
		padding: 0.35rem 0 0.35rem 1rem;
		border-left: 2px solid #00ff8833;
		margin-bottom: 0.5rem;
	}

	:global(.analysis-text p:last-child) {
		margin-bottom: 0;
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
		flex-wrap: wrap;
	}

	.footer-link {
		color: #00ff8877;
		text-decoration: none;
		transition: color 0.2s;
	}

	.footer-link:hover {
		color: #00ff88;
	}

	.share-bar {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin: 2rem 0 1.5rem;
		padding: 0.75rem 1rem;
		border: 1px solid #00ff8822;
		border-radius: 6px;
		background: #0f0f18;
	}

	.share-label {
		font-size: 0.6rem;
		letter-spacing: 0.2em;
		color: #00ff8855;
		margin-right: 0.5rem;
	}

	.share-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 36px;
		height: 36px;
		border-radius: 6px;
		border: 1px solid #00ff8811;
		background: transparent;
		color: #00ff8866;
		cursor: pointer;
		transition: all 0.2s;
		text-decoration: none;
	}

	.share-btn:hover {
		border-color: #00ff8844;
		color: #00ff88;
		background: #00ff8808;
	}

	.share-btn.twitter:hover { color: #1da1f2; border-color: #1da1f244; }
	.share-btn.facebook:hover { color: #1877f2; border-color: #1877f244; }
	.share-btn.reddit:hover { color: #ff4500; border-color: #ff450044; }
	.share-btn.copy:hover { color: #ffd700; border-color: #ffd70044; }

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