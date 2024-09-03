<slot />

<style>
	@import url('https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap');

	:global(body) {
		--color-text-on-primary: #ffffff;
		--color-primary: #328eff;
		--color-primary-light1: #95c5ff;
		--color-primary-light2: #c3deff;

		--color-background: #fafafa;
		--color-text: #222;

		--color-separator: #aaa;
		--color-hover: var(--color-primary-light1);
		--color-selected: var(--color-primary-light2);
	}

	:global(body) {
		font-family: 'Open Sans', Arial, sans-serif;
		color: var(--color-text);
		background-color: var(--color-background);

		height: 100vh;
		margin: 0;
		padding: 80px 24px;
		box-sizing: border-box;

		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	:global(input) {
		font: inherit;
		border-radius: 4px;
		padding: 8px 12px;
		border: 1px solid var(--color-separator);
	}

	:global(*) {
		transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
	}
</style>
