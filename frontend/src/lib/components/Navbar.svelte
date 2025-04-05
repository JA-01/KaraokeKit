<script lang="ts">
	import LightDarkToggle from '$lib/components/LightDarkToggle.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
</script>

<div class="sticky top-0 z-20 w-full border-b bg-background bg-opacity-75 backdrop-blur-md">
	<div class="container mx-auto flex items-center justify-between px-4 py-3 md:px-6">
		<Button variant="ghost" href="/" class="text-xl font-bold">KaraokeKit</Button>

		<!-- desktop nav -->
		<nav class="hidden items-center gap-4 md:flex">
			<!-- <Button href="/signup" variant="ghost">Sign Up</Button>
				<Button href="/login" variant="ghost">Log In</Button> -->
			<LightDarkToggle />
		</nav>
	</div>
</div>
