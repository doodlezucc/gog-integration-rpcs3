<script lang="ts" context="module">
	import { onMount } from 'svelte';
	import type { FileSystemEntityType } from './FileExplorerItemRow.svelte';

	export interface FileSystemRoot {
		identifier: string;
	}

	export interface FileSystemEntity {
		basename: string;
		type: FileSystemEntityType;
	}

	export interface FileExplorerController {
		listRoots(): Promise<FileSystemRoot[]>;
		listFilesInDirectory(directoryPath: string): Promise<FileSystemEntity[]>;
	}
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import FileExplorerItemRow from './FileExplorerItemRow.svelte';
	import TableRow from './TableRow.svelte';

	export let controller: FileExplorerController;
	export let path = '';

	$: userEnteredPath = path;

	let roots: FileSystemRoot[] = [];
	let files: FileSystemEntity[] = [];

	$: {
		if (path && browser) {
			controller.listFilesInDirectory(path).then((fetchedFiles) => (files = fetchedFiles));
		}
	}

	function onClickFile(file: FileSystemEntity) {
		if (file.type === 'directory') {
			files = [];
			path += '/' + file.basename;
		}
	}

	onMount(async () => {
		roots = await controller.listRoots();
	});
</script>

<div class="file-explorer">
	<input type="text" bind:value={userEnteredPath} />

	<div class="row">
		<div class="scroll-container">
			<table>
				{#each roots as root (root.identifier)}
					<TableRow selected={path.startsWith(root.identifier)}>
						<td>{root.identifier}</td>
					</TableRow>
				{/each}
			</table>
		</div>

		<div class="scroll-container expand">
			<table>
				{#each files as file}
					<FileExplorerItemRow
						name={file.basename}
						type={file.type}
						on:click={() => onClickFile(file)}
					/>
				{/each}
			</table>
		</div>
	</div>
</div>

<style>
	.file-explorer {
		background-color: white;
		box-shadow: 0 2px 4px #1113;

		display: flex;
		flex-direction: column;
		gap: 8px;
		padding: 16px;
		border-radius: 16px;
		min-height: 0;
	}

	.row {
		flex: 1;
		display: flex;
		flex-direction: row;
		gap: 8px;
		min-height: 0;
	}

	.expand {
		flex: 1;
	}

	.scroll-container {
		min-width: 128px;
		border: 1px solid var(--color-separator);
		border-radius: 4px;
		overflow: hidden auto;
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}
</style>
