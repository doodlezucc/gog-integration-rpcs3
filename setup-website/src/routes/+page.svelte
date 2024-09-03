<script>
	import FileExplorer from '$lib/FileExplorer.svelte';
	import { RemoteFileExplorerController } from '$lib/remote-file-explorer';

	const fileExplorerController = new RemoteFileExplorerController();
</script>

<main>
	<FileExplorer path="C:" controller={fileExplorerController} />
</main>

<style>
	main {
		width: 100%;
		max-width: 800px;
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	:global(main > *) {
		flex: 1;
	}
</style>
