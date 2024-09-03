<script lang="ts">
	export let selected = false;
</script>

<tr class:selected on:click>
	<slot />
</tr>

<style>
	tr {
		user-select: none;
		height: 36px;
		transition-duration: 0.3s;
	}

	tr.selected {
		background-color: var(--color-selected);
	}

	tr:hover {
		background-color: var(--color-hover);
		transition-duration: 0s;
	}

	:global(td) {
		padding: 0 8px;
	}
	:global(td:not(:last-child)) {
		padding-right: 0px;
	}
</style>
