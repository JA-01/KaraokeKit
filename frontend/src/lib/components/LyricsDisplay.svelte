<script lang="ts">
	import { onMount } from 'svelte';

	const { audioElement = null, audioFileName = '' } = $props<{
		audioElement: HTMLAudioElement | null;
		audioFileName: string;
	}>();

	// State
	let subtitles = $state<Array<{ id: number; start: number; end: number; text: string }>>([]);
	let currentLyric = $state<string>('');
	let nextLyric = $state<string>('');
	let isLoading = $state(true);
	let error = $state<string | null>(null);
	let isPlaying = $state(false);

	// Parse SRT from API endpoint
	async function loadSubtitlesFromApi() {
		if (!audioFileName) {
			isLoading = false;
			error = 'No audio file selected';
			return;
		}

		try {
			isLoading = true;
			error = null;

			const BACKEND_URL = 'https://40aa-66-129-246-4.ngrok-free.app';
			const response = await fetch(`${BACKEND_URL}/lyrics`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					text: audioFileName
				})
			});

			if (!response.ok) {
				throw new Error(`Failed to fetch lyrics: ${response.statusText}`);
			}

			const srtContent = await response.text();
			parseSubtitles(srtContent);
			isLoading = false;

			// Force an initial update of lyrics
			if (audioElement) {
				updateLyrics();
			}
		} catch (err) {
			console.error('Error loading subtitles:', err);
			isLoading = false;
			error = err instanceof Error ? err.message : 'Failed to load lyrics';
		}
	}

	// Parse SRT content to structured format
	function parseSubtitles(srtContent: string) {
		const blocks = srtContent.trim().split(/\n\s*\n/);

		subtitles = blocks
			.map((block) => {
				const lines = block.split('\n');
				if (lines.length < 3) return null; // Skip malformed blocks

				const id = parseInt(lines[0]);

				const timecodes = lines[1].split(' --> ');
				const start = timeToSeconds(timecodes[0]);
				const end = timeToSeconds(timecodes[1]);

				// Join the remaining lines as the text content
				const text = lines.slice(2).join('\n');

				return { id, start, end, text };
			})
			.filter((subtitle) => subtitle !== null) as Array<{
			id: number;
			start: number;
			end: number;
			text: string;
		}>;

		console.log('Parsed subtitles:', subtitles);

		// Set initial lyrics if available
		if (subtitles.length > 0) {
			nextLyric = subtitles[0].text;
		}
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
		if (!audioElement || subtitles.length === 0) return;

		const currentTime = audioElement.currentTime;

		// Find current subtitle
		const current = subtitles.find((sub) => currentTime >= sub.start && currentTime <= sub.end);

		// Find next subtitle
		const nextIndex = subtitles.findIndex((sub) => sub.start > currentTime);
		const next = nextIndex !== -1 ? subtitles[nextIndex] : null;

		currentLyric = current ? current.text : '';
		nextLyric = next ? next.text : '';

		// Debug
		console.log(
			`Current time: ${currentTime}, Current lyric: "${currentLyric}", Next lyric: "${nextLyric}"`
		);
	}

	// Setup audio time update listener
	function setupAudioListeners() {
		if (!audioElement) return;

		const updateHandler = () => {
			updateLyrics();
		};

		const playHandler = () => {
			isPlaying = true;
			updateLyrics();
		};

		const pauseHandler = () => {
			isPlaying = false;
		};

		audioElement.addEventListener('timeupdate', updateHandler);
		audioElement.addEventListener('play', playHandler);
		audioElement.addEventListener('pause', pauseHandler);

		return () => {
			audioElement?.removeEventListener('timeupdate', updateHandler);
			audioElement?.removeEventListener('play', playHandler);
			audioElement?.removeEventListener('pause', pauseHandler);
		};
	}

	// Watch for changes to the audioFileName
	$effect(() => {
		if (audioFileName) {
			loadSubtitlesFromApi();
		}
	});

	// Watch for changes to the audioElement
	$effect(() => {
		if (audioElement) {
			setupAudioListeners();
			updateLyrics(); // Initial update
		}
	});

	onMount(() => {
		const cleanup = setupAudioListeners();
		return cleanup;
	});
</script>

<div class="mt-4 w-full">
	{#if isLoading}
		<div class="flex justify-center py-4">
			<div class="text-gray-500">Loading lyrics...</div>
		</div>
	{:else if error}
		<div class="relative rounded border border-red-400 bg-red-100 px-4 py-3 text-red-700">
			<p class="font-bold">Error loading lyrics</p>
			<p class="text-sm">{error}</p>
		</div>
	{:else if subtitles.length === 0}
		<div class="rounded-lg bg-black/80 p-6 text-center">
			<p class="italic text-gray-400">No lyrics available</p>
		</div>
	{:else}
		<div class="rounded-lg bg-black/80 p-6 text-center">
			<div class="flex h-24 flex-col justify-center">
				{#if currentLyric}
					<p class="animate-pulse text-2xl font-bold text-white">{currentLyric}</p>
				{:else if isPlaying}
					<p class="italic text-gray-400">Waiting for lyrics...</p>
				{:else}
					<p class="italic text-gray-400">Play the audio to see lyrics</p>
				{/if}

				{#if nextLyric}
					<p class="mt-2 text-lg text-gray-400">{nextLyric}</p>
				{/if}
			</div>
		</div>
	{/if}
</div>
