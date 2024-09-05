<script lang="ts">
	import type { FileSystemEntity } from '$lib/FileExplorer.svelte';
	import { onMount } from 'svelte';
	import ExecutableDetectedDialog from './ExecutableDetectedDialog.svelte';
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
	let focusedFile: FileSystemEntity | null = null;
	let detectedExecutablePath: string | null = null;

	$: isValidRPCS3Directory = filesInDirectory.some(
		(fse) => fse.type === 'directory' && fse.basename === 'dev_hdd0'
	);
	$: isValidRPCS3Executable = focusedFile !== null;

	let configuration: Partial<RPCS3Configuration> = {};

	function detectExecutable() {
		const match = filesInDirectory.find(
			(fse) => fse.type === 'file' && fse.basename.toLowerCase() === 'rpcs3.exe'
		);

		if (match) {
			detectedExecutablePath = `${currentPath}/${match.basename}`;
		}
	}

	function submitDirectory() {
		if (currentPath && isValidRPCS3Directory) {
			configuration = {
				...configuration,
				configurationDirectory: currentPath
			};

			currentStep = ConfigurationStep.LocateExecutable;
			detectExecutable();
		}
	}

	function submitExecutable() {
		if (focusedFile && isValidRPCS3Executable) {
			const pathToExecutable = `${currentPath}/${focusedFile.basename}`;

			configuration = {
				...configuration,
				executable: pathToExecutable
			};

			submitConfiguration();
		}
	}

	function submitConfiguration() {
		if (detectedExecutablePath) {
			configuration = {
				...configuration,
				executable: detectedExecutablePath
			};
		}

		const queryParameters = new URLSearchParams(configuration);

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

		<Rpcs3FileExplorer hideFiles bind:currentPath bind:filesInDirectory>
			<button slot="submit-button" on:click={submitDirectory} disabled={!isValidRPCS3Directory}>
				Use Directory
			</button>
		</Rpcs3FileExplorer>
	</StepPage>
{:else if currentStep === ConfigurationStep.LocateExecutable}
	<StepPage title="Locate Your RPCS3 Application">
		<span slot="description">
			Select your RPCS3 executable in the file explorer. On Windows, this might be a file called
			"rpcs3.exe".
		</span>

		{#if detectedExecutablePath}
			<div class="dialog-container">
				<ExecutableDetectedDialog
					executablePath={detectedExecutablePath}
					on:clickOther={() => (detectedExecutablePath = null)}
					on:clickOK={() => submitConfiguration()}
				/>
			</div>
		{:else}
			<Rpcs3FileExplorer bind:focusedFile bind:currentPath bind:filesInDirectory>
				<button slot="submit-button" on:click={submitExecutable} disabled={!isValidRPCS3Executable}>
					Select
				</button>
			</Rpcs3FileExplorer>
		{/if}
	</StepPage>
{/if}

<style>
	.dialog-container {
		display: grid;
		align-items: start;
		justify-items: center;
		padding-top: 3em;
	}
</style>
