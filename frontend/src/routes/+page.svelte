<script lang="ts">
	import { Input } from '$lib/components/ui/input';
	import { buttonVariants } from '$lib/components/ui/button';
	import Dropzone from '$lib/components/Dropzone.svelte';

	let file = $state<File | null>(null);

	function handleFileChange(event: Event) {
		const input = event.target as HTMLInputElement;
		if (input.files && input.files.length > 0) {
			file = input.files[0];
			// TODO: Trigger upload or processing here
			console.log('Selected MP3:', input.files[0].name);
		}
	}
</script>

<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
	Welcome to KaraokeKit!
</h1>

<p class="leading-7 [&:not(:first-child)]:mt-6">To get started, upload your audio track.</p>

<Dropzone />
