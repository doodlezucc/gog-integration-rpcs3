<script lang="ts">
	import { fly } from 'svelte/transition';

	export let selected = false;
	export let staggeringIndex = 0;
</script>

<tr class:selected on:click in:fly={{ y: 10, delay: 20 * staggeringIndex }}>
	<slot />
</tr>

<style>
	:global(tr) {
		user-select: none;
		height: 28px;
		transition-duration: 0.3s;
	}

	:global(tr:hover) {
		background-color: var(--color-hover);
		color: var(--color-text);
		transition-duration: 0s;
	}

	:global(tr.selected) {
		background-color: var(--color-selected);
		color: var(--color-text-on-primary);
	}

	:global(td) {
		padding: 0 8px;
	}
	:global(td:not(:last-child)) {
		padding-right: 0px;
	}
</style>
