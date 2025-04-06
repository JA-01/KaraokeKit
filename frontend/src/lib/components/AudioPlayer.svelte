<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Slider } from '$lib/components/ui/slider';
	import { onMount } from 'svelte';

	export let src: string;

	let audio: HTMLAudioElement;
	let isPlaying = false;
	let duration = 0;
	let currentTime = 0;
	let animationFrame: number;

	function togglePlayback() {
		if (!audio) return;

		if (isPlaying) {
			audio.pause();
			cancelAnimationFrame(animationFrame);
		} else {
			audio.play();
			updateProgress();
		}
		isPlaying = !isPlaying;
	}

	function updateProgress() {
		currentTime = audio.currentTime;
		animationFrame = requestAnimationFrame(updateProgress);
	}

	function seek(time: number) {
		audio.currentTime = time;
		currentTime = time;
	}

	function formatTime(seconds: number): string {
		const minutes = Math.floor(seconds / 60)
			.toString()
			.padStart(2, '0');
		const secs = Math.floor(seconds % 60)
			.toString()
			.padStart(2, '0');
		return `${minutes}:${secs}`;
	}

	onMount(() => {
		audio.addEventListener('loadedmetadata', () => {
			duration = audio.duration;
		});

		audio.addEventListener('ended', () => {
			isPlaying = false;
			cancelAnimationFrame(animationFrame);
		});
	});
</script>

<div class="w-full max-w-xl rounded-xl border bg-white p-4 shadow-md dark:bg-zinc-900">
	<audio bind:this={audio} {src}></audio>

	<div class="flex items-center gap-4">
		<Button on:click={togglePlayback}>
			{#if isPlaying}
				Pause
			{:else}
				Play
			{/if}
		</Button>

		<div class="flex-1">
			<Slider
				min={0}
				max={duration}
				step={0.1}
				value={[currentTime]}
				on:change={(e) => seek(e.detail.value[0])}
			/>
		</div>

		<div class="text-sm tabular-nums text-gray-600 dark:text-gray-300">
			{formatTime(currentTime)} / {formatTime(duration)}
		</div>
	</div>
</div>
