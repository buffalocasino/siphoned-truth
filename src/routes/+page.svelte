<script lang="ts">
	import { page } from '$app/stores';

	let { data }: { data: { articles?: any[] } } = $props();
	let articles = $derived(data?.articles ?? []);
</script>

<svelte:head>
	<title>The Siphoned Truth</title>
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
			<span>AUTH: HERMES_AGENT_V4</span>
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
	{/if}

	<footer>
		<span>SEC_LEVEL: UNRESTRICTED_PUBLIC</span>
		<span>•</span>
		<span>SIG: SHADOW_NODE_01</span>
		<span>•</span>
		<span>AUTO-PUBLISH: ACTIVE</span>
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
		max-width: 1100px;
		margin: 0 auto;
		padding: 2rem;
	}

	header {
		text-align: center;
		padding: 3rem 0 2rem;
		border-bottom: 1px solid #00ff8833;
		margin-bottom: 2rem;
	}

	.logo-wrap {
		display: flex;
		justify-content: center;
		margin-bottom: 1rem;
	}

	.logo-img {
		height: 360px;
		width: auto;
	}

	h1 {
		font-size: 2.5rem;
		font-weight: 400;
		letter-spacing: 0.4em;
		color: #00ff88;
		margin: 0 0 0.5rem;
		text-shadow: 0 0 30px #00ff8844;
	}

	.subtitle {
		color: #00ff8877;
		font-size: 0.85rem;
		letter-spacing: 0.2em;
		margin: 0 0 1.5rem;
	}

	.stats {
		display: flex;
		gap: 1rem;
		justify-content: center;
		font-size: 0.65rem;
		color: #00ff8855;
		letter-spacing: 0.15em;
	}

	.loading, .empty {
		text-align: center;
		padding: 4rem;
		color: #00ff8866;
		font-size: 0.8rem;
		letter-spacing: 0.2em;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
		gap: 1.5rem;
	}

	.card {
		background: #0f0f18;
		border: 1px solid #00ff8822;
		text-decoration: none;
		color: inherit;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		transition: border-color 0.2s, box-shadow 0.2s;
	}

	.card:hover {
		border-color: #00ff8855;
		box-shadow: 0 0 20px #00ff8811;
	}

	.card-thumb {
		width: 100%;
		height: 160px;
		background-size: cover;
		background-position: center;
		background-color: #0f0f18;
		flex-shrink: 0;
	}

	.card-body {
		padding: 1.25rem 1.5rem 1.5rem;
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.card-id {
		font-size: 0.6rem;
		color: #00ff8855;
		letter-spacing: 0.2em;
		margin-bottom: 0.5rem;
	}

	.card h2 {
		font-size: 0.95rem;
		font-weight: 400;
		color: #00ff88;
		margin: 0 0 0.75rem;
		letter-spacing: 0.05em;
	}

	.card-narrative {
		font-size: 0.75rem;
		color: #00ff8899;
		line-height: 1.6;
		margin: 0 0 1rem;
		flex: 1;
	}

	.card-meta {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
		font-size: 0.6rem;
		color: #00ff8855;
		letter-spacing: 0.1em;
	}

	.verdict-tag {
		color: #ff4444;
	}

	footer {
		margin-top: 4rem;
		padding-top: 1.5rem;
		border-top: 1px solid #00ff8822;
		display: flex;
		gap: 1rem;
		justify-content: center;
		font-size: 0.6rem;
		color: #00ff8833;
		letter-spacing: 0.15em;
	}
</style>