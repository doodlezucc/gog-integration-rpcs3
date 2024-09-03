import type {
	FileExplorerController,
	FileSystemEntity,
	FileSystemRoot
} from './FileExplorer.svelte';

export class RemoteFileExplorerController implements FileExplorerController {
	private async fetchJson(endpoint: string) {
		const response = await fetch(endpoint);

		return await response.json();
	}

	async listFilesInDirectory(): Promise<FileSystemEntity[]> {
		return [
			{
				basename: 'example-directory',
				type: 'directory'
			},
			{
				basename: 'rpcs3.exe',
				type: 'file'
			}
		];
	}

	async listRoots(): Promise<FileSystemRoot[]> {
		return [{ identifier: 'C:' }, { identifier: 'D:' }];
	}
}
