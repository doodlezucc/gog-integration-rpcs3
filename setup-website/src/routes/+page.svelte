<script>
	import { RestConnection } from '$lib/rest';

	const rest = new RestConnection('http://localhost:1619/api');

	async function openFolderViaRest() {
		const { rpcs3Path } = await rest.locateRPCS3();

		console.log(rpcs3Path);
	}
</script>

<button on:click={openFolderViaRest}>Pick your RPCS3 directory</button>
