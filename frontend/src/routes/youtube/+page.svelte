<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Loader2, Recycle } from 'lucide-svelte';
	import LyricsDisplay from '$lib/components/LyricsDisplay.svelte';
	import { Input } from '$lib/components/ui/input';

	let url = $state<string>('');
	let processedAudioUrl = $state<string | null>(null);
	let initiatedProcessing = $state(false);
	let audioElement = $state<HTMLAudioElement | null>(null);

	const BACKEND_URL = 'https://6f62-66-129-246-4.ngrok-free.app';

	async function uploadFile() {
		if (!url) return;

		try {
			initiatedProcessing = true;

			const response = await fetch(`${BACKEND_URL}/ytdl`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ url })
			});

			if (!response.ok) {
				console.error('Failed to process audio:', await response.text());
				initiatedProcessing = false;
				return;
			}

			const blob = await response.blob();
			processedAudioUrl = URL.createObjectURL(blob);
			initiatedProcessing = false;
		} catch (error) {
			console.error('Error uploading file:', error);
			initiatedProcessing = false;
		}
	}
	function handleAudioLoaded(event: Event) {
		audioElement = event.target as HTMLAudioElement;
	}

	function reset() {
		// Clean up resources
		if (processedAudioUrl) {
			URL.revokeObjectURL(processedAudioUrl);
		}

		// Reset all state variables
		url = '';
		processedAudioUrl = null;
		initiatedProcessing = false;
		audioElement = null;
	}
</script>

<h1
	class="scroll-m-20 text-4xl font-extrabold tracking-tight text-black dark:text-white lg:text-5xl"
>
	Welcome to KaraokeKit!
</h1>

{#if processedAudioUrl && url}
	<div class="mt-6 w-full max-w-xl rounded-xl bg-white p-4 shadow-md dark:bg-zinc-900">
		<audio class="w-full" controls onloadedmetadata={handleAudioLoaded}>
			<source src={processedAudioUrl} type="audio/mpeg" />
			Your browser does not support the audio element.
		</audio>

		<LyricsDisplay {audioElement} audioFileName={processedAudioUrl} youtubeUrl={url} />

		<div class="mt-4">
			<Button onclick={reset} class="gap-2">
				<Recycle class="h-4 w-4" /> Upload New URL
			</Button>
		</div>
	</div>
{:else}
	<p class="leading-7 text-gray-800 dark:text-gray-300 [&:not(:first-child)]:mt-6">
		To get started, paste a YouTube link below:
	</p>
	<div class="mx-auto flex w-full max-w-xl flex-col items-center gap-4 p-6">
		<Input
			type="url"
			bind:value={url}
			class="rounded-lg border border-pink-300 bg-pink-100 text-pink-900 placeholder-pink-600 shadow-sm transition
			       focus:border-pink-500 focus:ring-2 focus:ring-pink-400
			       dark:border-pink-700 dark:bg-pink-950 dark:text-pink-100 dark:placeholder-pink-400
			       dark:focus:border-pink-400 dark:focus:ring-pink-600"
		/>

		{#if initiatedProcessing}
			<Button disabled={true}>
				<Loader2 class="h-4 w-4 animate-spin" />Processing YouTube video...</Button
			>
		{:else}
			<Button onclick={uploadFile} disabled={!url}>Process YouTube Video</Button>
		{/if}
	</div>
{/if}
