<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';
	let { children } = $props();
	const gaId = import.meta.env.VITE_GA_ID || '';
</script>

<svelte:head>
	{#if gaId}
		<script async src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}></script>
		<script>
			window.dataLayer = window.dataLayer || [];
			function gtag(){dataLayer.push(arguments);}
			gtag('js', new Date());
			gtag('config', gaId);
		</script>
	{/if}
	<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1032028091690286" crossorigin="anonymous"></script>
	<meta name="google-adsense-account" content="ca-pub-1032028091690286" />
	<link rel="icon" href={favicon} />
	<meta property="og:site_name" content="The Siphoned Truth" />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="The Siphoned Truth" />
	<meta property="og:description" content="Adversarial synthesis of elite deception via raw OSINT telemetry" />
	<meta property="og:url" content="https://blog-iota-gray-35.vercel.app" />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:site" content="@_Norvell_" />
	<link rel="canonical" href="https://blog-iota-gray-35.vercel.app" />
</svelte:head>

{@render children()}