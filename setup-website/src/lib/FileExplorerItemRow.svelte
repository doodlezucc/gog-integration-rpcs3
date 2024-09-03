<script lang="ts" context="module">
	export type FileSystemEntityType = 'file' | 'directory';
</script>

<script lang="ts">
	import Icon from './Icon.svelte';
	import FolderRegular from './icons/FolderRegular.svelte';
	import PlayStation from './icons/PlayStation.svelte';

	export let type: FileSystemEntityType;
	export let name: string;
</script>

<td align="center"><Icon Component={type === 'file' ? PlayStation : FolderRegular} /></td>
<td><span>{name}</span></td>

<style>
	td:first-child {
		width: 20px;
	}
</style>
