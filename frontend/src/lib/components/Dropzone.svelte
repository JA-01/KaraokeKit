<script lang="ts">
	import { Button } from '$lib/components/ui/button';

	let file = $state<File | null>(null);
	let isDragging = $state(false);

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

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		const selectedFile = input.files?.[0];
		if (selectedFile && selectedFile.type.startsWith('audio/')) {
			file = selectedFile;
		}
	}

	function triggerFileSelect() {
		const input = document.getElementById('file-upload') as HTMLInputElement;
		input?.click();
	}
</script>

<div class="mx-auto flex w-full max-w-xl flex-col items-center gap-4 p-6">
	<div
		class={`flex h-48 w-full cursor-pointer flex-col items-center
            justify-center rounded-xl border-2 border-dashed px-4 text-center transition-colors
            ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white dark:bg-black/10'}`}
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

	<Button on:click={triggerFileSelect}>Choose File</Button>
</div>
