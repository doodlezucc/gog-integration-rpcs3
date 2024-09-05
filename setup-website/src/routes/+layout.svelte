<slot />

<style>
	@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

	:global(body) {
		--color-text-on-primary: #ffffff;
		--color-primary: #0d68d8;
		--color-primary-dark1: #0c52a8;
		--color-primary-dark2: #154177;
		--color-primary-light1: #95c5ff;
		--color-primary-light2: #c3deff;

		--color-background: #ffffff;
		--color-text: #222;

		--color-separator: #aaa;
		--color-disabled: #666;
		--color-hover: var(--color-primary-light1);
		--color-selected: var(--color-primary-light2);
	}

	:global(body) {
		font-family: 'Open Sans', Arial, sans-serif;
		color: var(--color-text);
		background-color: var(--color-background);

		height: 100vh;
		margin: 0;
		box-sizing: border-box;
		display: flex;
		flex-direction: column;
	}

	:global(h1) {
		margin: 0;
		font-size: 1.75em;
		font-weight: normal;
		color: var(--color-primary);
	}

	:global(input, button) {
		font: inherit;
		border: none;
		border-radius: 6px;
	}

	:global(input) {
		padding: 8px 12px;
		border: 1px solid var(--color-separator);
	}

	:global(button) {
		transition: 0.3s;
	}

	:global(button:enabled) {
		cursor: pointer;
	}

	:global(button:not(.icon)) {
		background-color: var(--color-primary);
		color: var(--color-text-on-primary);
		padding: 8px 24px 10px;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		box-shadow: 0 -4px 0 #1115 inset;
	}

	:global(button:not(.icon):disabled) {
		background-color: var(--color-disabled);
		opacity: 0.5;
	}

	:global(button:enabled:hover) {
		background-color: var(--color-primary-dark1);
		transition-duration: 0.05s;
	}

	:global(button:enabled:active) {
		background-color: var(--color-primary-dark2);
	}

	:global(*) {
		transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
	}
</style>
