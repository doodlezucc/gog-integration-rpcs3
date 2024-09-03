<script>
	import FileExplorer from '$lib/FileExplorer.svelte';
	import { RemoteFileExplorerController } from '$lib/remote-file-explorer';

	const fileExplorerController = new RemoteFileExplorerController('http://localhost:1619/api');
</script>

<main>
	<FileExplorer path="C:/" controller={fileExplorerController} />
</main>

<style>
	main {
		width: 100%;
		max-width: 800px;
		min-height: 0;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	:global(main > *) {
		flex: 1;
	}
</style>
