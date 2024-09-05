<script lang="ts">
	import { fly } from 'svelte/transition';

	export let title: string;
</script>

<main>
	<h1 in:fly={{ y: 10 }}>{title}</h1>
	<p in:fly={{ y: 10, delay: 100 }}>
		<slot name="description" />
	</p>

	<slot />
</main>

<style>
	main {
		display: grid;
		grid-template-rows: min-content min-content auto;
		min-height: 0;
		flex: 1;
		margin: 16px;
	}

	h1,
	p {
		text-align: center;
	}

	p {
		font-size: 1em;
		margin: 0;
		padding-bottom: 1.5em;
		color: var(--color-disabled);
	}
</style>
