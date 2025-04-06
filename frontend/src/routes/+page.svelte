<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Loader2, Recycle } from 'lucide-svelte';
	import LyricsDisplay from '$lib/components/LyricsDisplay.svelte';

	let file = $state<File | null>(null);
	let isDragging = $state(false);
	let processedAudioUrl = $state<string | null>(null);
	let initiatedProcessing = $state(false);
	let audioElement = $state<HTMLAudioElement | null>(null);

	function handleDrop(event: DragEvent) {
		event.preventDefault();
		isDragging = false;
		const droppedFile = event.dataTransfer?.files?.[0];
		if (droppedFile && droppedFile.type.startsWith('audio/')) {
			file = droppedFile;
		}
	}

	function handleDragOver(event: DragEvent) {
		event.preventDefault();
		isDragging = true;
	}

	function handleDragLeave() {
		isDragging = false;
	}

	function triggerFileSelect() {
		const input = document.getElementById('file-upload') as HTMLInputElement;
		input?.click();
	}

	async function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const selectedFile = input.files?.[0];
		if (selectedFile && selectedFile.type.startsWith('audio/')) {
			file = selectedFile;
		}
	}

	const BACKEND_URL = 'https://40aa-66-129-246-4.ngrok-free.app';

	async function uploadFile() {
		if (!file) return;

		const formData = new FormData();
		formData.append('file', file);

		try {
			initiatedProcessing = true;
			const response = await fetch(`${BACKEND_URL}/process`, {
				method: 'POST',
				body: formData
			});

			if (!response.ok) {
				console.error('Failed to process audio:', await response.text());
				initiatedProcessing = false;
				return;
			}

			// get audio file from response
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
		file = null;
		processedAudioUrl = null;
		initiatedProcessing = false;
		audioElement = null;

		// Reset file input value
		const input = document.getElementById('file-upload') as HTMLInputElement;
		if (input) input.value = '';
	}
</script>

<h1
	class="scroll-m-20 text-4xl font-extrabold tracking-tight text-black dark:text-white lg:text-5xl"
>
	Welcome to KaraokeKit!
</h1>

{#if processedAudioUrl && file}
	<div class="mt-6 w-full max-w-xl rounded-xl bg-white p-4 shadow-md dark:bg-zinc-900">
		<audio class="w-full" controls onloadedmetadata={handleAudioLoaded}>
			<source src={processedAudioUrl} type="audio/mpeg" />
			Your browser does not support the audio element.
		</audio>

		<LyricsDisplay {audioElement} audioFileName={file.name} />

		<div class="mt-4">
			<Button onclick={reset} class="gap-2">
				<Recycle class="h-4 w-4" /> Upload New Track
			</Button>
		</div>
	</div>
{:else}
	<p class="leading-7 text-gray-800 dark:text-gray-300 [&:not(:first-child)]:mt-6">
		To get started, upload your audio track.
	</p>
	<div class="mx-auto flex w-full max-w-xl flex-col items-center gap-4 p-6">
		<div
			class="flex h-48 w-full cursor-pointer flex-col items-center
            justify-center rounded-xl border-2 border-dashed px-4 text-center transition-colors
            {isDragging
				? 'border-blue-500 bg-blue-50'
				: 'border-gray-300 bg-white dark:bg-black/10'}"
			onclick={triggerFileSelect}
			ondragover={handleDragOver}
			ondragleave={handleDragLeave}
			ondrop={handleDrop}
		>
			<p class="text-base font-medium text-gray-700 dark:text-gray-300">
				{isDragging ? 'Drop your audio file here' : 'Drag & drop your audio here'}
			</p>
			<p class="mt-1 text-sm text-gray-500">or click to upload (MP3, WAV, OGG)</p>
		</div>

		<input
			id="file-upload"
			type="file"
			accept="audio/mpeg, audio/wav, audio/ogg, audio/flac, audio/m4a"
			class="hidden"
			onchange={handleFileChange}
		/>

		{#if file}
			<div class="mt-2 text-sm text-gray-600 dark:text-gray-300">
				Selected: {file.name}
			</div>
		{/if}

		{#if !file}
			<Button onclick={triggerFileSelect}>Choose File</Button>
		{:else if initiatedProcessing}
			<Button disabled={true}>
				<Loader2 class="h-4 w-4 animate-spin" /> Processing audio file...</Button
			>
		{:else}
			<Button onclick={uploadFile} disabled={!file}>Process Audio</Button>
		{/if}
	</div>
{/if}
