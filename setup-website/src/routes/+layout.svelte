<slot />

<style global>
	@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

	body {
		--color-text-on-primary: #ffffff;
		--color-primary: #0d68d8;
		--color-primary-dark1: #0c52a8;
		--color-primary-dark2: #154177;
		--color-shade-light1: #a8a8a8;
		--color-shade-light2: #e2e2e2;

		--color-background: #ffffff;
		--color-text: #222;

		--color-separator: #aaa;
		--color-disabled: #666;
		--color-hover: var(--color-shade-light2);
		--color-active: var(--color-shade-light1);
		--color-selected: var(--color-primary);
	}

	body {
		font-family: 'Open Sans', Arial, sans-serif;
		color: var(--color-text);
		background-color: var(--color-background);

		height: 100vh;
		margin: 0;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
	}

	h1,
	h2 {
		margin: 0;
		font-weight: normal;
		color: var(--color-primary);
	}

	h1 {
		font-size: 1.75em;
	}

	input,
	button {
		font: inherit;
		border: none;
		border-radius: 6px;
	}

	input {
		padding: 8px 12px;
		border: 1px solid var(--color-separator);
	}

	button {
		transition: 0.3s;
	}

	button:enabled {
		cursor: pointer;
	}

	button:not(.icon) {
		background-color: var(--color-primary);
		color: var(--color-text-on-primary);
		padding: 8px 24px;
	}

	button:not(.icon):disabled {
		background-color: var(--color-disabled);
		opacity: 0.5;
	}

	button:enabled:hover {
		background-color: var(--color-primary-dark1);
		transition-duration: 0.05s;
	}

	button:enabled:active {
		background-color: var(--color-primary-dark2);
	}

	button.shallow {
		background-color: white;
		color: var(--color-text);
	}

	button.shallow:hover {
		background-color: var(--color-hover);
	}

	button.shallow:active {
		background-color: var(--color-active);
	}

	* {
		transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
	}

	header {
		background-color: var(--color-primary);
		text-align: center;
		color: var(--color-text-on-primary);
		padding: 0.5em;
	}
</style>
