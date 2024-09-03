<script lang="ts" context="module">
	export type FileSystemEntityType = 'file' | 'directory';
</script>

<script lang="ts">
	import Icon from './Icon.svelte';
	import FolderRegular from './icons/FolderRegular.svelte';
	import PlayStation from './icons/PlayStation.svelte';
	import TableRow from './TableRow.svelte';

	export let type: FileSystemEntityType;
	export let name: string;
</script>

<TableRow on:click>
	<td align="center"><Icon Component={type === 'file' ? PlayStation : FolderRegular} /></td>
	<td><span>{name}</span></td>
</TableRow>

<style>
	td:first-child {
		width: 20px;
	}
</style>
