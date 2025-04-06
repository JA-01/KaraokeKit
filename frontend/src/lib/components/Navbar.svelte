<script lang="ts">
	import LightDarkToggle from '$lib/components/LightDarkToggle.svelte';
	import Button from '$lib/components/ui/button/button.svelte';

	let isMenuOpen = false;
</script>

<div class="sticky top-0 z-20 w-full border-b border-pink-400 bg-pink-300 bg-opacity-75 backdrop-blur-md dark:bg-pink-900">
	<div class="container mx-auto flex items-center justify-between px-4 py-3 md:px-6">
		<Button variant="ghost" href="/" class="text-xl font-bold">KaraokeKit</Button>

		<!-- desktop nav -->
		<nav class="hidden items-center gap-4 md:flex">
			<Button href="/youtube" variant="ghost" class="">YouTube Generator</Button>
			<Button href="/about" variant="ghost" class="">About</Button>
			<Button href="/how-to-use" variant="ghost" class="">How to Use</Button>
			<LightDarkToggle />
		</nav>

		<!-- mobile nav -->
		<div class="relative flex items-center gap-4 md:hidden">
			<LightDarkToggle />

            <button
                class="text-pink-900 dark:text-pink-100 focus:outline-none z-30"
                on:click={() => (isMenuOpen = !isMenuOpen)}
            >
                {#if isMenuOpen}
                    <span>&#x2715; <!-- Close Icon --></span>
                {:else}
                    <span>&#9776; <!-- Hamburger Icon --></span>
                {/if}
            </button>

            
            {#if isMenuOpen}
            <nav
                class="absolute right-0 top-full mt-2 w-48 rounded-lg bg-pink-300 py-2 shadow-lg dark:bg-pink-800 z-20"
            >
                <Button href="/youtube" variant="ghost" class="block w-full text-left px-4 py-2">YouTube Generator</Button>
                <Button href="/about" variant="ghost" class="block w-full text-left px-4 py-2">About</Button>
                <Button href="/how-to-use" variant="ghost" class="block w-full text-left px-4 py-2">How to Use</Button>
            </nav>
            {/if}
        </div>
	</div>
</div>
