<script lang="ts">
	let { data }: { data: { articles?: any[]; page?: number; totalPages?: number; totalArticles?: number } } = $props();

	let articles = $derived(data?.articles ?? []);
	let page = $derived(data?.page ?? 1);
	let totalPages = $derived(data?.totalPages ?? 1);
	let totalArticles = $derived(data?.totalArticles ?? 0);
</script>

<svelte:head>
	<title>The Siphoned Truth {page > 1 ? `— Page ${page}` : ''}</title>
	<meta name="description" content="Adversarial synthesis of elite deception via raw OSINT telemetry" />
</svelte:head>

<main>
	<header>
		<div class="logo-wrap">
			<img src="/logo.svg" alt="The Siphoned Truth" class="logo-img" />
		</div>
		<p class="subtitle">Adversarial OSINT Intelligence Bureau</p>
		<div class="stats">
			<span>FEEDS: 60+ ACTIVE</span>
			<span>•</span>
			<span>LAYERS: 35 CONCURRENT</span>
			<span>•</span>
			<a href="/map" class="stat-link">▸ HEATMAP</a>
			<span>•</span>
			<a href="https://deflock.org" target="_blank" rel="noopener" class="stat-link">▸ DEFLOCK MAP</a>
		</div>
	</header>

	{#if articles.length === 0}
		<div class="empty">
			<p>[NO ACTIVE REPORTS]</p>
			<p>ShadowBroker telemetry feed pending. Reports generate at 0800, 1200, 1600 EST.</p>
		</div>
	{:else}
		<div class="grid">
			{#each articles as article}
				<a href="/article/{article.slug ?? article.id}" class="card">
					<div class="card-thumb" style="background-image: url('/covers/{article.slug?.toLowerCase() ?? article.id?.toLowerCase()}.jpg')"></div>
					<div class="card-body">
						<div class="card-id">{article.id}</div>
						<h2>{article.title}</h2>
						<p class="card-narrative">{String(article.narrative ?? article.article_body ?? article.content ?? article.summary ?? '').slice(0, 120)}...</p>
						<div class="card-meta">
							<span>{article.time ?? ''}</span>
							<span class="verdict-tag">{String(article.verdict ?? '').slice(0, 60)}...</span>
						</div>
					</div>
				</a>
			{/each}
		</div>

		<!-- Pagination -->
		{#if totalPages > 1}
			<nav class="pagination">
				{#if page > 1}
					<a href="/" class="page-btn">«</a>
					<a href="/page/{page - 1}" class="page-btn">‹</a>
				{/if}

				{#each Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
					const start = Math.max(1, Math.min(page - 3, totalPages - 6));
					return start + i;
				}) as p}
					{#if p <= totalPages}
						<a href={p === 1 ? '/' : `/page/${p}`} class="page-btn" class:active={p === page}>{p}</a>
					{/if}
				{/each}

				{#if page < totalPages}
					<a href="/page/{page + 1}" class="page-btn">›</a>
					<a href="/page/{totalPages}" class="page-btn">»</a>
				{/if}

				<span class="page-info">Page {page} of {totalPages} · {totalArticles} reports</span>
			</nav>
		{/if}
	{/if}

	<footer>
		<span>SIG: SHADOW_NODE_01</span>
		<span>•</span>
		<span>AUTO-PUBLISH: ACTIVE</span>
		<span>•</span>
		<a href="/map" class="footer-link">▸ INTERACTIVE HEATMAP</a>
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
		padding: 2rem;
	}

	header {
		text-align: center;
		margin-bottom: 3rem;
	}

	.logo-wrap {
		margin-bottom: 0.5rem;
	}

	.logo-img {
		height: 64px;
	}

	.subtitle {
		color: #00ff8877;
		font-size: 0.7rem;
		letter-spacing: 0.3em;
		margin: 0.25rem 0 1.5rem;
	}

	.stats {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
		align-items: center;
		flex-wrap: wrap;
		font-size: 0.65rem;
		letter-spacing: 0.15em;
		color: #00ff8866;
	}

	.stat-link {
		color: #00ff88;
		text-decoration: none;
	}

	.stat-link:hover {
		color: #00ffaa;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 1.5rem;
		margin-bottom: 3rem;
	}

	.card {
		background: #0f0f18;
		border: 1px solid #00ff8822;
		text-decoration: none;
		display: block;
		transition: border-color 0.2s;
	}

	.card:hover {
		border-color: #00ff8866;
	}

	.card-thumb {
		height: 180px;
		background-size: cover;
		background-position: center;
		background-color: #1a1a2e;
	}

	.card-body {
		padding: 1.25rem;
	}

	.card-id {
		font-size: 0.6rem;
		color: #00ff8844;
		letter-spacing: 0.2em;
		margin-bottom: 0.5rem;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	h2 {
		font-size: 0.9rem;
		font-weight: 400;
		color: #00ff88;
		margin: 0 0 0.75rem;
		line-height: 1.4;
		letter-spacing: 0.05em;
	}

	.card-narrative {
		font-size: 0.78rem;
		color: #00ff8899;
		line-height: 1.6;
		margin: 0 0 0.75rem;
	}

	.card-meta {
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		font-size: 0.65rem;
		color: #00ff8855;
	}

	.verdict-tag {
		color: #ff4444aa;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.pagination {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.4rem;
		flex-wrap: wrap;
		margin: 2rem 0;
		padding: 1.5rem;
		border: 1px solid #00ff8811;
		background: #0f0f18;
	}

	.page-btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 2.2rem;
		height: 2.2rem;
		padding: 0 0.5rem;
		background: #1a1a2e;
		border: 1px solid #00ff8833;
		color: #00ff88aa;
		text-decoration: none;
		font-size: 0.8rem;
		transition: all 0.15s;
	}

	.page-btn:hover {
		background: #00ff8822;
		color: #00ff88;
		border-color: #00ff8866;
	}

	.page-btn.active {
		background: #00ff8822;
		color: #00ff88;
		border-color: #00ff88;
		font-weight: 700;
	}

	.page-info {
		font-size: 0.65rem;
		color: #00ff8855;
		letter-spacing: 0.1em;
		margin-left: 0.5rem;
	}

	footer {
		border-top: 1px solid #00ff8811;
		padding-top: 1.5rem;
		display: flex;
		gap: 0.75rem;
		align-items: center;
		flex-wrap: wrap;
		font-size: 0.65rem;
		color: #00ff8855;
		letter-spacing: 0.1em;
		justify-content: center;
	}

	.footer-link {
		color: #00ff88;
		text-decoration: none;
	}

	.footer-link:hover {
		color: #00ffaa;
	}
</style>
