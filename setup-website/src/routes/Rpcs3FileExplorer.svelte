<script lang="ts">
	import { browser } from '$app/environment';
	import type { FileSystemEntity } from '$lib/FileExplorer.svelte';
	import FileExplorer from '$lib/FileExplorer.svelte';
	import { RemoteFileExplorerController } from '$lib/remote-file-explorer';

	export let hideFiles: boolean = false;
	export let focusedFile: FileSystemEntity | null = null;

	const VALID_EXTENSIONS = ['.exe', '.app', '.AppImage'];

	const fileExplorerController = new RemoteFileExplorerController(
		'http://localhost:1619/api',
		(file) => {
			if (file.type === 'directory') return true;

			const fileName = file.basename;
			return VALID_EXTENSIONS.some((ext) => fileName.endsWith(ext));
		}
	);

	function getDirectoryFromURL() {
		if (!browser) return undefined;

		const hash = window.location.hash;

		if (hash.includes('#')) {
			return decodeURIComponent(hash.substring(1));
		}
	}

	export let currentPath = getDirectoryFromURL();
	export let filesInDirectory: FileSystemEntity[] = [];
</script>

<svelte:window on:popstate={() => (currentPath = getDirectoryFromURL())} />

<FileExplorer
	{hideFiles}
	bind:focusedFile
	bind:path={currentPath}
	bind:files={filesInDirectory}
	controller={fileExplorerController}
>
	<slot name="submit-button" slot="submit-button" />
</FileExplorer>
