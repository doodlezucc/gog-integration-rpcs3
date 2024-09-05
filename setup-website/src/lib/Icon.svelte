<script lang="ts">
	import type { SvelteComponent } from 'svelte';

	export let Component: typeof SvelteComponent<Record<string, never>>;
</script>

<i class="icon" role="presentation">
	<svelte:component this={Component} />
</i>

<style>
	:global(i.icon) {
		display: block;
		height: 1em;
	}

	:global(i.icon svg) {
		height: inherit;
		fill: currentColor;
	}
</style>
