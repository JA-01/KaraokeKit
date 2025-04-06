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

<div
	class={`min-h-screen bg-gradient-to-br text-white ${
		isDarkMode ? 'from-gray-900 via-pink-900 to-black' : 'text-black from-purple-300 via-pink-200 to-red-300'
	}`}
>
	<main class="flex flex-col items-center justify-center px-6 py-12">
		{@render children()}
	</main>
</div>
