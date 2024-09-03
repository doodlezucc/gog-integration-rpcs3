import type {
	FileExplorerController,
	FileSystemEntity,
	FileSystemRoot
} from './FileExplorer.svelte';

export class RemoteFileExplorerController implements FileExplorerController {
	readonly baseUrl: string;

	constructor(baseUrl: string) {
		this.baseUrl = baseUrl;
	}

	private async fetchJson(endpoint: string) {
		const response = await fetch(this.baseUrl + endpoint);
		return await response.json();
	}

	async listFilesInDirectory(directory: string): Promise<FileSystemEntity[]> {
		return await this.fetchJson(`/list?directory=${directory}`);
	}

	async listRoots(): Promise<FileSystemRoot[]> {
		return await this.fetchJson('/roots');
	}
}
