<script lang="ts">
	import type { FileSystemEntity } from '$lib/FileExplorer.svelte';
	import { onMount } from 'svelte';
	import Rpcs3FileExplorer from './Rpcs3FileExplorer.svelte';
	import StepPage from './StepPage.svelte';

	interface RPCS3Configuration {
		configurationDirectory: string;
		executable: string;
	}

	enum ConfigurationStep {
		LocateConfigurationDirectory = 0,
		LocateExecutable = 1
	}

	const stepCount = 2;
	let currentStep: ConfigurationStep;

	let currentPath: string;
	let filesInDirectory: FileSystemEntity[] = [];
	let focusedFile: FileSystemEntity | undefined;

	$: isValidRPCS3Directory = filesInDirectory.some(
		(fse) => fse.type === 'directory' && fse.basename === 'dev_hdd0'
	);
	$: isValidRPCS3Executable = false;

	let configuration: Partial<RPCS3Configuration> = {};

	function submitDirectory() {
		if (currentPath && isValidRPCS3Directory) {
			configuration = {
				...configuration,
				configurationDirectory: currentPath
			};

			currentStep = ConfigurationStep.LocateExecutable;
			currentPath = currentPath + '';
		}
	}

	function submitConfiguration() {
		const queryParameters = new URLSearchParams({
			configurationDirectory: ''
		});

		window.location.href = `/callback?${queryParameters}`;
	}

	onMount(() => {
		currentStep = ConfigurationStep.LocateConfigurationDirectory;
	});
</script>

<header>
	<span>
		{#if currentStep !== undefined}
			Step {currentStep + 1}/{stepCount}
		{:else}
			Step 1/{stepCount}
		{/if}
	</span>
</header>

{#if currentStep === ConfigurationStep.LocateConfigurationDirectory}
	<StepPage title="Locate Your RPCS3 Directory">
		<span slot="description">
			The <i>RPCS3 directory</i> contains PS3 sub-directories such as "dev_hdd0" and similar.
		</span>

		<Rpcs3FileExplorer bind:currentPath bind:filesInDirectory>
			<button slot="submit-button" on:click={submitDirectory} disabled={!isValidRPCS3Directory}>
				Use Directory
			</button>
		</Rpcs3FileExplorer>
	</StepPage>
{:else if currentStep === ConfigurationStep.LocateExecutable}
	<StepPage title="Locate Your RPCS3 Executable">
		<span slot="description">
			Navigate to your RPCS3 application. On Windows, this might be a file called "rpcs3.exe".
		</span>

		<Rpcs3FileExplorer bind:currentPath bind:filesInDirectory>
			<button
				slot="submit-button"
				on:click={submitConfiguration}
				disabled={!isValidRPCS3Executable}
			>
				Select
			</button>
		</Rpcs3FileExplorer>
	</StepPage>
{/if}

<style>
	header {
		background-color: var(--color-primary);
		text-align: center;
		color: var(--color-text-on-primary);
		padding: 0.5em;
	}
</style>
