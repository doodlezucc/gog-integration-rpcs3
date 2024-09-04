interface LocateRPCS3Response {
	rpcs3Path: string | null;
}

export class RestConnection {
	private readonly baseUrl: string;

	constructor(baseUrl: string) {
		this.baseUrl = baseUrl;
	}

	private async fetchJson(endpoint: string) {
		const response = await fetch(this.baseUrl + endpoint);
		return await response.json();
	}

	async locateRPCS3(): Promise<LocateRPCS3Response> {
		return await this.fetchJson('/locate-rpcs3');
	}
}
