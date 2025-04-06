<script lang="ts">
	import LightDarkToggle from '$lib/components/LightDarkToggle.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<div
	class="sticky top-0 z-20 w-full border-b border-pink-400 bg-pink-300 bg-opacity-75 backdrop-blur-md dark:bg-pink-900"
>
	<div class="container mx-auto flex items-center justify-between px-4 py-3 md:px-6">
		<Button variant="ghost" href="/" class="text-xl font-bold">KaraokeKit</Button>

		<!-- desktop nav -->
		<nav class="hidden items-center gap-4 md:flex">
			<!-- <Button href="/signup" variant="ghost">Sign Up</Button>
				<Button href="/login" variant="ghost">Log In</Button> -->
			<Button href="/about" variant="ghost" class="">About</Button>
			<Button href="/how-to-use" variant="ghost" class="">How to Use</Button>
			<LightDarkToggle />
		</nav>
	</div>
</div>
