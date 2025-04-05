<script lang="ts">
	import Navbar from '$lib/components/Navbar.svelte';
	import '../app.css';

	import { ModeWatcher } from 'mode-watcher';

	let { children } = $props();
</script>

<ModeWatcher />
<Navbar />

<main class="px-16 py-6">
	{@render children()}
</main>
