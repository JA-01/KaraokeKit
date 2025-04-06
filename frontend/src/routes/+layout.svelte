<script lang="ts">
	import Navbar from '$lib/components/Navbar.svelte';
	import { onMount } from 'svelte';
	import '../app.css';

	import { ModeWatcher, setMode } from 'mode-watcher';

	let { children } = $props();

	let isDarkMode = $state(false);
	onMount(() => {
		isDarkMode = document.documentElement.classList.contains('dark');

		const observer = new MutationObserver(() => {
			isDarkMode = document.documentElement.classList.contains('dark');
		});
		observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
		return () => observer.disconnect();
	});
</script>

<ModeWatcher />
<Navbar />

<div>
	<main class="flex flex-col items-center justify-center px-6 py-12">
		{@render children()}
	</main>
</div>
