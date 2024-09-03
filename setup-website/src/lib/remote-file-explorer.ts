import type {
	FileExplorerController,
	FileSystemEntity,
	FileSystemRoot
} from './FileExplorer.svelte';

export class RemoteFileExplorerController implements FileExplorerController {
	readonly baseUrl: string;
	private readonly fileFilter: (fse: FileSystemEntity) => boolean;

	constructor(baseUrl: string, fileFilter: (fse: FileSystemEntity) => boolean) {
		this.baseUrl = baseUrl;
		this.fileFilter = fileFilter;
	}

	filterFileSystemEntity(fse: FileSystemEntity): boolean {
		return this.fileFilter(fse);
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
