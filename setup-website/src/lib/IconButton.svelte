<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import Icon from './Icon.svelte';

	export let Component: typeof SvelteComponent<Record<string, never>>;
</script>

<button on:click>
	<Icon {Component} />
</button>

<style>
	button {
		width: 40px;
		height: 40px;
		border-radius: 4px;
		border: 1px solid var(--color-separator);
	}
</style>
