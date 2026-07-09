<script lang="ts">
	import { onMount } from 'svelte';
	// Redirect to page 1 — the pagination route handles the full article feed
	onMount(() => {
		window.location.replace('/page/1');
	});
</script>

<svelte:head>
	<title>The Siphoned Truth</title>
	<meta http-equiv="refresh" content="0; url=/page/1" />
</svelte:head>

<div class="loading">
	<a href="/page/1">→ Enter</a>
</div>

<style>
	:global(body) {
		background: #0a0a0f;
		color: #00ff88;
		font-family: 'Courier New', monospace;
		margin: 0;
		min-height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.loading {
		text-align: center;
	}
	a {
		color: #00ff88;
		text-decoration: none;
		font-size: 1.2rem;
		letter-spacing: 0.2em;
	}
</style>
