<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import type { MapPin } from './types';

	interface Props {
		pins: MapPin[];
	}

	let { pins }: Props = $props();

	let container: HTMLDivElement | undefined = $state();
	let mounted = $state(false);
	let hoverPin = $state<MapPin | null>(null);
	let hoverPos = $state({ x: 0, y: 0 });
	let mapInstance: any = null;
	let deckInstance: any = null;

	function formatTime(iso: string): string {
		if (!iso) return '';
		try {
			const d = new Date(iso);
			return d.toISOString().slice(0, 10);
		} catch {
			return iso;
		}
	}

	onMount(async () => {
		// All deck.gl + maplibre imports are client-only.
		let maplibre: any;
		let Deck: any;
		let ScatterplotLayer: any;
		try {
			const maplibreModule = await import('maplibre-gl');
			maplibre = maplibreModule.default ?? maplibreModule;
			const deckCore = await import('@deck.gl/core');
			Deck = deckCore.Deck;
			const deckLayers = await import('@deck.gl/layers');
			ScatterplotLayer = deckLayers.ScatterplotLayer;
		} catch (err) {
			console.error('[SiphonedTruth/Map] Failed to load map libraries:', err);
			// Surface a visible error so the user knows what happened
			if (container) {
				const el = container.parentElement;
				if (el) {
					el.innerHTML = `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#0a0a0f;color:#ff4444;font-family:'Courier New',monospace;font-size:0.75rem;letter-spacing:0.15em;text-align:center;padding:2rem;">[ MAP LIBRARY LOAD FAILED — CHECK CONSOLE ]<br><br><span style="color:#ff444488;font-size:0.6rem;">${String(err).replace(/</g, '&lt;')}</span></div>`;
				}
			}
			return;
		}

		// Dark terminal-themed basemap. No API key required.
		// Carto dark_matter is MIT-licensed, served as raster tiles, free for any use.
		const style: any = {
			version: 8,
			sources: {
				'carto-dark': {
					type: 'raster',
					tiles: [
						'https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
						'https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
						'https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png',
						'https://d.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png'
					],
					tileSize: 256,
					attribution: '© OpenStreetMap contributors © CARTO'
				}
			},
			layers: [
				{
					id: 'carto-dark-layer',
					type: 'raster',
					source: 'carto-dark',
					paint: { 'raster-opacity': 0.85 }
				}
			]
		};

		mapInstance = new maplibre.Map({
			container: container!,
			style,
			center: [10, 30],
			zoom: 1.5,
			minZoom: 1,
			maxZoom: 12,
			attributionControl: false,
			fadeDuration: 0
		});

		mapInstance.addControl(new maplibre.NavigationControl({ showCompass: false }), 'top-right');

		// Deck.gl overlay sharing the map's WebGL context.
		const overlay = new Deck({
			canvas: 'siphoned-truth-deck-canvas',
			width: '100%',
			height: '100%',
			initialViewState: {
				longitude: 10,
				latitude: 30,
				zoom: 1.5,
				bearing: 0,
				pitch: 0
			},
			controller: true,
			onViewStateChange: ({ viewState }: any) => {
				mapInstance.jumpTo({
					center: [viewState.longitude, viewState.latitude],
					zoom: viewState.zoom,
					bearing: viewState.bearing,
					pitch: viewState.pitch
				});
			},
			layers: [
				new ScatterplotLayer({
					id: 'investigations',
					data: pins,
					pickable: true,
					opacity: 0.95,
					stroked: true,
					filled: true,
					radiusUnits: 'pixels',
					radiusMinPixels: 4,
					radiusMaxPixels: 18,
					getPosition: (d: MapPin) => [d.lon, d.lat],
					getRadius: (d: MapPin) => 6 + Math.min(d.telemetryCount, 8) * 0.6,
					getFillColor: () => [0, 255, 136, 220],
					getLineColor: () => [0, 255, 136, 255],
					lineWidthMinPixels: 1.5,
					onHover: (info: any) => {
						if (info?.object) {
							hoverPin = info.object as MapPin;
							hoverPos = { x: info.x, y: info.y };
						} else {
							hoverPin = null;
						}
					},
					onClick: (info: any) => {
						if (info?.object?.slug) {
							goto(`/article/${info.object.slug}`);
						}
					},
					updateTriggers: {
						getRadius: [pins.length]
					}
				})
			]
		});

		// Sync mouse cursor: pointer over pins, default elsewhere
		const mapCanvas = mapInstance.getCanvas();
		if (mapCanvas) mapCanvas.style.cursor = 'default';
		const deckCanvas = overlay.getCanvas?.();
		if (deckCanvas) deckCanvas.style.cursor = 'default';

		const setCursor = (cur: string) => {
			if (mapInstance) mapInstance.getCanvas().style.cursor = cur;
			const deckCanvas = overlay.getCanvas?.();
			if (deckCanvas) deckCanvas.style.cursor = cur;
		};

		// The deck overlay absorbs pointer events, so listen there for hover
		overlay.setProps({
			onHover: (info: any) => {
				if (info?.object) {
					hoverPin = info.object as MapPin;
					hoverPos = { x: info.x, y: info.y };
					setCursor('pointer');
				} else {
					hoverPin = null;
					setCursor('default');
				}
			}
		});

		deckInstance = overlay;
		mounted = true;
	});

	onDestroy(() => {
		try {
			deckInstance?.finalize?.();
		} catch {
			/* noop */
		}
		try {
			mapInstance?.remove?.();
		} catch {
			/* noop */
		}
	});
</script>

<div class="map-frame">
	<div class="map-header">
		<div class="map-title">
			<span class="bracket">[</span>INVESTIGATION HEATMAP<span class="bracket">]</span>
		</div>
		<div class="map-stats">
			<span>{pins.length} PINS</span>
			<span>•</span>
			<span>{new Set(pins.map((p) => p.region)).size} REGIONS</span>
		</div>
	</div>

	<div class="map-wrap">
		<div bind:this={container} class="maplibre-host"></div>
		<canvas id="siphoned-truth-deck-canvas" class="deck-canvas"></canvas>

		{#if !mounted}
			<div class="loading">
				<div class="spinner">▮▮▮</div>
				<p>[ INITIALIZING GLOBE LAYER... ]</p>
			</div>
		{/if}

		{#if hoverPin}
			<div
				class="tooltip"
				style="transform: translate({hoverPos.x + 16}px, {hoverPos.y + 16}px);"
			>
				<div class="tip-region">▸ {hoverPin.region}</div>
				<div class="tip-title">{hoverPin.title}</div>
				<div class="tip-meta">
					<span>{hoverPin.id}</span>
					<span class="dot">•</span>
					<span>{formatTime(hoverPin.time)}</span>
				</div>
				{#if hoverPin.preview}
					<div class="tip-preview">{hoverPin.preview}{hoverPin.preview.length >= 160 ? '…' : ''}</div>
				{/if}
				<div class="tip-cta">CLICK TO OPEN DOSSIER ▸</div>
			</div>
		{/if}
	</div>

	<div class="map-legend">
		<span class="legend-dot"></span>
		<span>Each pin = one investigation. Pin size ∝ telemetry point count.</span>
	</div>
</div>

<style>
	.map-frame {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.map-header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		padding: 0.75rem 1rem;
		border: 1px solid #00ff8822;
		background: #0f0f18;
		font-family: 'Courier New', monospace;
	}

	.map-title {
		color: #00ff88;
		font-size: 0.75rem;
		letter-spacing: 0.3em;
		text-shadow: 0 0 12px #00ff8844;
	}

	.bracket {
		color: #00ff8855;
		margin: 0 0.4em;
	}

	.map-stats {
		color: #00ff8855;
		font-size: 0.6rem;
		letter-spacing: 0.2em;
		display: flex;
		gap: 0.5rem;
	}

	.map-wrap {
		position: relative;
		width: 100%;
		height: 70vh;
		min-height: 480px;
		border: 1px solid #00ff8822;
		background: #050507;
		overflow: hidden;
	}

	.maplibre-host,
	.deck-canvas {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
	}

	.deck-canvas {
		pointer-events: auto;
		z-index: 2;
	}

	.maplibre-host {
		z-index: 1;
	}

	.loading {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: #050507;
		color: #00ff8888;
		font-family: 'Courier New', monospace;
		z-index: 5;
		font-size: 0.75rem;
		letter-spacing: 0.2em;
	}

	.spinner {
		color: #00ff88;
		font-size: 1.5rem;
		letter-spacing: 0.5em;
		margin-bottom: 0.5rem;
		animation: pulse 1.2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 0.4; }
		50% { opacity: 1; }
	}

	.tooltip {
		position: absolute;
		top: 0;
		left: 0;
		width: 320px;
		max-width: 80vw;
		background: #0a0a0fcc;
		border: 1px solid #00ff8888;
		padding: 0.85rem 1rem;
		font-family: 'Courier New', monospace;
		color: #00ff88;
		pointer-events: none;
		z-index: 10;
		box-shadow: 0 0 30px #00ff8822;
		backdrop-filter: blur(4px);
	}

	.tip-region {
		font-size: 0.6rem;
		color: #00ff8888;
		letter-spacing: 0.2em;
		margin-bottom: 0.4rem;
	}

	.tip-title {
		font-size: 0.85rem;
		color: #00ff88;
		line-height: 1.4;
		margin-bottom: 0.4rem;
	}

	.tip-meta {
		font-size: 0.6rem;
		color: #00ff8855;
		letter-spacing: 0.15em;
		display: flex;
		gap: 0.4rem;
		margin-bottom: 0.6rem;
	}

	.dot { color: #00ff8833; }

	.tip-preview {
		font-size: 0.7rem;
		color: #00ff88aa;
		line-height: 1.6;
		margin-bottom: 0.6rem;
	}

	.tip-cta {
		font-size: 0.6rem;
		color: #00ff88;
		letter-spacing: 0.25em;
		border-top: 1px dashed #00ff8833;
		padding-top: 0.5rem;
		text-align: right;
	}

	.map-legend {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		font-family: 'Courier New', monospace;
		font-size: 0.6rem;
		color: #00ff8866;
		letter-spacing: 0.15em;
		padding: 0.5rem 1rem;
	}

	.legend-dot {
		width: 8px;
		height: 8px;
		background: #00ff88;
		border-radius: 50%;
		box-shadow: 0 0 6px #00ff88;
	}
</style>
