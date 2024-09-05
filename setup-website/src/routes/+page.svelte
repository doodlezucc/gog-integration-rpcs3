<script lang="ts">
	import { browser } from '$app/environment';
	import type { FileSystemEntity } from '$lib/FileExplorer.svelte';
	import FileExplorer from '$lib/FileExplorer.svelte';
	import { RemoteFileExplorerController } from '$lib/remote-file-explorer';

	const VALID_RPCS3_FILE_NAMES = ['rpcs3.exe', 'rpcs3'];

	const fileExplorerController = new RemoteFileExplorerController(
		'http://localhost:1619/api',
		(file) => {
			if (file.type === 'directory') return true;

			const fileName = file.basename.toLowerCase();
			return VALID_RPCS3_FILE_NAMES.includes(fileName);
		}
	);

	function getDirectoryFromURL() {
		if (!browser) return undefined;

		const hash = window.location.hash;

		if (hash.includes('#')) {
			return decodeURIComponent(hash.substring(1));
		}
	}

	let currentPath = getDirectoryFromURL();
	let filesInDirectory: FileSystemEntity[] = [];

	$: isValidRPCS3Root = filesInDirectory.some(
		(fse) => fse.type === 'directory' && fse.basename === 'dev_hdd0'
	);

	function submitDirectory() {
		if (currentPath && isValidRPCS3Root) {
			const queryParameters = new URLSearchParams({
				configurationDirectory: ''
			});

			window.location.href = `/callback?${queryParameters}`;
		}
	}
</script>

<svelte:window on:popstate={() => (currentPath = getDirectoryFromURL())} />

<main>
	<h1>Locate your RPCS3 Directory</h1>

	<FileExplorer
		bind:path={currentPath}
		bind:files={filesInDirectory}
		controller={fileExplorerController}
	></FileExplorer>

	<div class="bottom-bar">
		<button on:click={submitDirectory} disabled={!isValidRPCS3Root}>Use Directory</button>
	</div>
</main>

<style>
	main {
		display: grid;
		gap: 8px;
		grid-template-rows: min-content auto min-content;
		min-height: 0;
	}

	.bottom-bar {
		place-self: end;
	}
</style>
