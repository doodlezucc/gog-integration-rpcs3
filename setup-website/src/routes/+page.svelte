<script>
	import { browser } from '$app/environment';
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
</script>

<svelte:window on:popstate={() => (currentPath = getDirectoryFromURL())} />

<FileExplorer bind:path={currentPath} controller={fileExplorerController} />
