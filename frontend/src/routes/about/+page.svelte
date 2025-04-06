<script lang="ts">
	import { goto } from "$app/navigation";

</script>

<div class="bg-white bg-opacity-10 backdrop-blur-md rounded-lg shadow-lg p-8 max-w-3xl text-center">
    <h1 class="text-5xl font-extrabold mb-6 text-yellow-300 drop-shadow-lg">
        About KaraokeKit
    </h1>
    <p class="text-lg leading-relaxed">
        KaraokeKit is a platform designed to help you create and enjoy karaoke tracks. 
        Upload your audio files, and let our advanced algorithms process them to remove vocals and enhance the music.
    </p>
    <p class="text-lg leading-relaxed mt-4">
        We'll display the lyrics on the screen, so you can sing along with your favorite songs without the vocals.
        Whether you're hosting a karaoke night or just want to sing your heart out at home, KaraokeKit has you covered.
    </p>
    <div class="mt-8">
        <button
            class="bg-yellow-300 text-purple-800 font-bold py-2 px-6 rounded-full shadow-md hover:bg-yellow-400 transition"
            on:click={() => goto('')}
        >
            Get Started
        </button>
    </div>
</div>