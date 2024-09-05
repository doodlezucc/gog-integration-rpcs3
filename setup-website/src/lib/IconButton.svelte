<script lang="ts">
	import type { SvelteComponent } from 'svelte';
	import Icon from './Icon.svelte';

	export let Component: typeof SvelteComponent<Record<string, never>>;
</script>

<button class="icon shallow" on:click>
	<Icon {Component} />
</button>

<style>
	button {
		width: 40px;
		height: 40px;
		border-radius: 4px;
		border: 1px solid var(--color-separator);
		background-color: white;
	}

	button:hover {
		background-color: var(--color-hover);
	}

	button:active {
		background-color: var(--color-active);
	}
</style>
