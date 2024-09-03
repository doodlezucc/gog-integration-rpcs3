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
		filterFileSystemEntity(fse: FileSystemEntity): boolean;
	}
</script>

<script lang="ts">
	import { browser } from '$app/environment';
	import { pushState, replaceState } from '$app/navigation';
	import FileExplorerItemRow from './FileExplorerItemRow.svelte';
	import TableRow from './TableRow.svelte';

	export let controller: FileExplorerController;
	export let path: string | undefined = undefined;

	$: userEnteredPath = path;

	let roots: FileSystemRoot[] = [];
	let allFiles: FileSystemEntity[] = [];

	$: {
		if (path && browser) {
			allFiles = [];
			controller.listFilesInDirectory(path).then((fetchedFiles) => (allFiles = fetchedFiles));
		}
	}

	function pushDirectory(directoryName: string) {
		if (path && !path.endsWith('/')) {
			path += '/';
		}

		path += directoryName;
		pushState(`#${path}`, { directory: path! });
	}

	function onClickFile(file: FileSystemEntity) {
		if (file.type === 'directory') {
			pushDirectory(file.basename);
		}
	}

	$: filteredFiles = allFiles.filter((fse) => controller.filterFileSystemEntity(fse));
	$: filteredFilesSorted = [...filteredFiles].sort((a, b) => {
		if (a.type !== b.type) {
			return a.type === 'directory' ? -1 : 1;
		}

		return a.basename.localeCompare(b.basename);
	});

	function pushRoot(root: FileSystemRoot) {
		const previousPath = path;

		path = root.identifier;
		if (!path.includes('/')) {
			path += '/';
		}

		if (previousPath === undefined) {
			replaceState(`#${path}`, { directory: path! });
		} else {
			pushState(`#${path}`, { directory: path! });
		}
	}

	onMount(async () => {
		roots = await controller.listRoots();

		if (path === undefined) {
			pushRoot(roots[0]);
		}
	});
</script>

<div class="file-explorer">
	<input type="text" bind:value={userEnteredPath} />

	<div class="row">
		<div class="scroll-container">
			<table>
				{#each roots as root (root.identifier)}
					<TableRow on:click={() => pushRoot(root)} selected={path?.startsWith(root.identifier)}>
						<td>{root.identifier}</td>
					</TableRow>
				{/each}
			</table>
		</div>

		<div class="scroll-container expand">
			<table>
				{#each filteredFilesSorted as file, index}
					<TableRow staggeringIndex={index} on:click={() => onClickFile(file)}>
						<FileExplorerItemRow name={file.basename} type={file.type} />
					</TableRow>
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
