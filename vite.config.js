import { sveltekit } from '@sveltejs/kit/vite';

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	// Keep deck.gl + maplibre out of SSR. They pull in @luma.gl/webgl
	// which references `window` at module load.
	ssr: {
		external: ['@deck.gl/core', '@deck.gl/layers', 'maplibre-gl']
	}
};

export default config;
