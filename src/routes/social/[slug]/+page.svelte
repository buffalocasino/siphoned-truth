<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const article = $derived(data.article);

	const narrative = $derived(
		(article.narrative ?? article.article_body ?? article.content ?? article.summary ?? '').toString()
	);

	// Trim verdict to a shareable length
	const verdict = $derived(() => {
		const v = article.verdict ?? '';
		if (v.length <= 280) return v;
		// Cut at last sentence before 280
		const trimmed = v.slice(0, 280);
		const lastPeriod = trimmed.lastIndexOf('.');
		return lastPeriod > 100 ? trimmed.slice(0, lastPeriod + 1) : trimmed.trim() + '…';
	});

	// Pull a punchy excerpt from the narrative — first substantive sentence
	const excerpt = $derived(() => {
		const text = narrative.replace(/\*\*/g, '').replace(/\n+/g, ' ').trim();
		if (text.length <= 200) return text;
		// Find first period or sentence break
		const first = text.slice(0, 220);
		const lastSpace = first.lastIndexOf(' ');
		return first.slice(0, lastSpace) + '…';
	});

	const shareUrl = $derived(
		`https://siphonedtruth.online/article/${article.slug?.toLowerCase() ?? article.id.toLowerCase()}`
	);

	const coverUrl = $derived(
		article.coverImage ||
		`https://siphonedtruth.online/covers/${(article.slug?.toLowerCase() ?? article.id.toLowerCase())}.jpg`
	);

	const tags = $derived(
		(Array.isArray(article.tags) ? article.tags : [])
			.filter((t: string) => t.length > 2 && t.length < 30)
			.slice(0, 6)
	);

	const timeLabel = $derived(() => {
		try {
			return new Date(article.time).toLocaleDateString('en-US', {
				month: 'short',
				day: 'numeric',
				year: 'numeric'
			});
		} catch {
			return article.time;
		}
	});

	const categoryLabel = $derived(
		article.category ? `#${article.category.replace(/\s+/g, '')}` : '#OSINT'
	);
</script>

<svelte:head>
	<title>{article.title} | The Siphoned Truth</title>
	<meta name="description" content={excerpt()} />
	<meta property="og:title" content={article.title} />
	<meta property="og:description" content={excerpt()} />
	<meta property="og:type" content="article" />
	<meta property="og:url" content={shareUrl} />
	<meta property="og:image" content={coverUrl} />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="article:published_time" content={article.time} />
	<meta property="article:section" content={article.category || 'OSINT'} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={article.title} />
	<meta name="twitter:description" content={excerpt()} />
	<meta name="twitter:image" content={coverUrl} />
</svelte:head>

<div class="social-page">
	<!-- Cover image — full width top -->
	<div class="cover-wrap">
		<img src={coverUrl} alt={article.title} class="cover-img" />
		<div class="cover-overlay">
			<span class="site-badge">THE SIPHONED TRUTH</span>
			<span class="category-badge">{categoryLabel}</span>
		</div>
	</div>

	<!-- Article body -->
	<main class="content">
		<h1 class="headline">{article.title}</h1>

		<div class="byline">
			<time>{timeLabel()}</time>
			<span class="sep">·</span>
			<span class="read-time">OSINT ANALYSIS</span>
		</div>

		<!-- Verdict — styled as a pull quote -->
		<blockquote class="verdict-strip">
			<span class="verdict-label">THE VERDICT</span>
			<p>{verdict()}</p>
		</blockquote>

		<!-- Narrative excerpt -->
		<p class="excerpt">{excerpt()}</p>

		<!-- Tags -->
		{#if tags.length > 0}
			<div class="tags">
				{#each tags as tag}
					<span class="tag">#{tag}</span>
				{/each}
			</div>
		{/if}

		<!-- Share buttons -->
		<div class="share-section">
			<p class="share-prompt">SHARE THIS REPORT</p>
			<div class="share-buttons">
				<a
					href="https://www.facebook.com/sharer/sharer.php?u={encodeURIComponent(shareUrl)}"
					target="_blank"
					rel="noopener"
					class="share-btn facebook"
				>
					<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
						<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
					</svg>
					Facebook
				</a>
				<a
					href="https://twitter.com/intent/tweet?url={encodeURIComponent(shareUrl)}&text={encodeURIComponent(article.title)}&via=_Norvell_"
					target="_blank"
					rel="noopener"
					class="share-btn twitter"
				>
					<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
						<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
					</svg>
					Post to X
				</a>
				<a
					href="https://www.linkedin.com/sharing/share-offsite/?url={encodeURIComponent(shareUrl)}"
					target="_blank"
					rel="noopener"
					class="share-btn linkedin"
				>
					<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
						<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
					</svg>
					LinkedIn
				</a>
				<a
					href="https://www.reddit.com/submit?url={encodeURIComponent(shareUrl)}&title={encodeURIComponent(article.title)}"
					target="_blank"
					rel="noopener"
					class="share-btn reddit"
				>
					<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
						<path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z"/>
					</svg>
					Reddit
				</a>
			</div>
		</div>

		<!-- CTA to full article -->
		<a href={shareUrl} class="read-more">
			READ THE FULL OSINT REPORT →
		</a>
	</main>
</div>

<style>
	:global(body) {
		margin: 0;
		background: #f8f7f4;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
	}

	.social-page {
		max-width: 680px;
		margin: 0 auto;
		background: #ffffff;
		min-height: 100vh;
	}

	/* ── Cover ── */
	.cover-wrap {
		position: relative;
		width: 100%;
		aspect-ratio: 1200 / 630;
		overflow: hidden;
		background: #1a1a2e;
	}

	.cover-img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}

	.cover-overlay {
		position: absolute;
		top: 1rem;
		left: 1rem;
		display: flex;
		gap: 0.5rem;
		align-items: center;
	}

	.site-badge {
		background: #0a0a0a;
		color: #f8f7f4;
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		padding: 0.3rem 0.6rem;
		border-radius: 2px;
	}

	.category-badge {
		background: #c8102e;
		color: #ffffff;
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		padding: 0.3rem 0.6rem;
		border-radius: 2px;
	}

	/* ── Content ── */
	.content {
		padding: 2rem 2.5rem 3rem;
	}

	.headline {
		font-size: 1.65rem;
		font-weight: 700;
		color: #0a0a0a;
		line-height: 1.25;
		margin: 1.75rem 0 0.75rem;
		letter-spacing: -0.01em;
	}

	.byline {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		color: #888;
		font-size: 0.8rem;
		margin-bottom: 1.5rem;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
	}

	.time {
		color: #666;
	}

	.sep {
		color: #ccc;
	}

	.read-time {
		color: #888;
		text-transform: uppercase;
		letter-spacing: 0.08em;
		font-size: 0.72rem;
	}

	/* ── Verdict strip ── */
	.verdict-strip {
		background: #0a0a0a;
		border-left: 4px solid #c8102e;
		margin: 0 0 1.5rem;
		padding: 1.25rem 1.5rem;
		border-radius: 0 4px 4px 0;
	}

	.verdict-label {
		display: block;
		color: #c8102e;
		font-size: 0.62rem;
		font-weight: 700;
		letter-spacing: 0.18em;
		margin-bottom: 0.5rem;
	}

	.verdict-strip p {
		color: #f8f7f4;
		font-size: 0.97rem;
		line-height: 1.65;
		margin: 0;
		font-style: normal;
	}

	/* ── Excerpt ── */
	.excerpt {
		color: #333;
		font-size: 1.05rem;
		line-height: 1.75;
		margin: 0 0 1.5rem;
	}

	/* ── Tags ── */
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		margin-bottom: 2rem;
	}

	.tag {
		background: #f0efec;
		color: #555;
		font-size: 0.72rem;
		padding: 0.25rem 0.6rem;
		border-radius: 2px;
		letter-spacing: 0.03em;
	}

	/* ── Share section ── */
	.share-section {
		border-top: 1px solid #e8e7e4;
		padding-top: 1.5rem;
		margin-bottom: 2rem;
	}

	.share-prompt {
		color: #aaa;
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.15em;
		margin: 0 0 0.85rem;
		text-transform: uppercase;
	}

	.share-buttons {
		display: flex;
		flex-wrap: wrap;
		gap: 0.6rem;
	}

	.share-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.45rem;
		padding: 0.6rem 1.1rem;
		border-radius: 4px;
		font-size: 0.82rem;
		font-weight: 600;
		text-decoration: none;
		transition: opacity 0.15s, transform 0.1s;
		border: none;
		cursor: pointer;
	}

	.share-btn:hover {
		opacity: 0.85;
		transform: translateY(-1px);
	}

	.share-btn.facebook {
		background: #1877f2;
		color: #ffffff;
	}

	.share-btn.twitter {
		background: #0a0a0a;
		color: #ffffff;
	}

	.share-btn.linkedin {
		background: #0077b5;
		color: #ffffff;
	}

	.share-btn.reddit {
		background: #ff4500;
		color: #ffffff;
	}

	/* ── Read more ── */
	.read-more {
		display: block;
		text-align: center;
		background: #0a0a0a;
		color: #f8f7f4;
		text-decoration: none;
		padding: 0.9rem 1.5rem;
		border-radius: 4px;
		font-size: 0.82rem;
		font-weight: 600;
		letter-spacing: 0.08em;
		transition: background 0.15s;
	}

	.read-more:hover {
		background: #1a1a2e;
	}
</style>
