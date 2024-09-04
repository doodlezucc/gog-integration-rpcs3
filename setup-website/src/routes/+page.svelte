<script lang="ts">
	import { goto } from '$app/navigation';
	import { RestConnection } from '$lib/rest';

	const rest = new RestConnection('http://localhost:1619/api');

	async function openFolderViaRest() {
		const response = await rest.locateRPCS3();

		console.log(response);

		const queryParameters = <Record<string, string>>{ ...response };
		const queryParametersString = new URLSearchParams(queryParameters).toString();

		goto(`/callback?${queryParametersString}`);
	}
</script>

<button on:click={openFolderViaRest}>Pick your RPCS3 directory</button>
