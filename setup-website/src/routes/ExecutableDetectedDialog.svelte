<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	import { fly } from 'svelte/transition';

	export let executablePath: string;

	const dispatch = createEventDispatcher<{
		clickOther: undefined;
		clickOK: undefined;
	}>();

	let isMounted = false;
	onMount(() => (isMounted = true));
</script>

{#if isMounted}
	<div class="dialog" in:fly={{ y: 20, delay: 300 }}>
		<h2>Already Done</h2>
		<p>The RPCS3 application was <b>automatically detected</b> at <i>{executablePath}</i>.</p>
		<p>
			If this is not the executable you usually use to launch games, you may select a different
			file.
		</p>

		<div class="row">
			<button class="shallow" on:click={() => dispatch('clickOther')}>Select Other</button>
			<button on:click={() => dispatch('clickOK')}>OK</button>
		</div>
	</div>
{/if}

<style>
	.dialog {
		box-shadow: 0 4px 6px #1115;
		padding: 24px;
		border-radius: 8px;
	}

	p {
		max-width: 500px;
	}

	.row {
		display: grid;
		gap: 8px;
		grid-template-columns: max-content max-content;
		justify-content: end;
	}
</style>
