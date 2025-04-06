<script lang="ts">
	import { onMount } from 'svelte';

	// Props using Svelte 5's $props
	const { audioElement = null } = $props<{
		audioElement: HTMLAudioElement | null;
	}>();

	// State
	let subtitles = $state<Array<{ id: number; start: number; end: number; text: string }>>([]);
	let currentLyric = $state<string>('');
	let nextLyric = $state<string>('');
	let isLoading = $state(true);

	// Parse SRT file
	async function loadSubtitles() {
		try {
			const response = await fetch('/subtitles.srt');
			if (!response.ok) {
				throw new Error('Failed to load subtitles');
			}

			const srtContent = await response.text();
			parseSubtitles(srtContent);
			isLoading = false;
		} catch (error) {
			console.error('Error loading subtitles:', error);
			isLoading = false;
		}
	}

	// Parse SRT content to structured format
	function parseSubtitles(srtContent: string) {
		const blocks = srtContent.trim().split(/\n\s*\n/);

		subtitles = blocks.map((block) => {
			const lines = block.split('\n');
			const id = parseInt(lines[0]);

			const timecodes = lines[1].split(' --> ');
			const start = timeToSeconds(timecodes[0]);
			const end = timeToSeconds(timecodes[1]);

			// Join the remaining lines as the text content
			const text = lines.slice(2).join('\n');

			return { id, start, end, text };
		});
	}

	// Convert SRT timestamp to seconds
	function timeToSeconds(timeString: string): number {
		const [hours, minutes, secondsAndMs] = timeString.split(':');
		const [seconds, milliseconds] = secondsAndMs.split(',');

		return (
			parseInt(hours) * 3600 +
			parseInt(minutes) * 60 +
			parseInt(seconds) +
			parseInt(milliseconds) / 1000
		);
	}

	// Update current lyric based on audio time
	function updateLyrics() {
		console.log('updateLyrics');
		if (!audioElement) return;

		const currentTime = audioElement.currentTime;

		// Find current subtitle
		const current = subtitles.find((sub) => currentTime >= sub.start && currentTime <= sub.end);

		// Find next subtitle
		const nextIndex = subtitles.findIndex((sub) => sub.start > currentTime);
		const next = nextIndex !== -1 ? subtitles[nextIndex] : null;

		currentLyric = current ? current.text : '';
		nextLyric = next ? next.text : '';
	}

	// Setup audio time update listener
	function setupAudioListeners() {
		if (!audioElement) return;

		audioElement.addEventListener('timeupdate', updateLyrics);

		return () => {
			audioElement?.removeEventListener('timeupdate', updateLyrics);
		};
	}

	onMount(() => {
		loadSubtitles();
		const cleanup = setupAudioListeners();

		return cleanup;
	});
</script>

<div class="mt-4 w-full">
	{#if isLoading}
		<div class="flex justify-center py-4">
			<div class="text-gray-500">Loading lyrics...</div>
		</div>
	{:else}
		<div class="rounded-lg bg-black/80 p-6 text-center">
			<div class="flex h-24 flex-col justify-center">
				{#if currentLyric}
					<p class="animate-pulse text-2xl font-bold text-white">{currentLyric}</p>
				{:else}
					<p class="italic text-gray-400">Waiting for lyrics...</p>
				{/if}

				{#if nextLyric}
					<p class="mt-2 text-lg text-gray-400">{nextLyric}</p>
				{/if}
			</div>
		</div>
	{/if}
</div>
