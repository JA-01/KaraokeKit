<script lang="ts">
	import { goto } from "$app/navigation";

</script>

<div class="bg-white bg-opacity-10 backdrop-blur-md rounded-lg shadow-lg p-8 max-w-3xl text-center">
    <h1 class="text-5xl font-extrabold mb-6 text-white-300 drop-shadow-lg">
        About KaraokeKit
    </h1>
    <p class="text-lg leading-relaxed">
        KaraokeKit is a powerful and easy-to-use platform that transforms any song into a karaoke track. 
        With KaraokeKit, you can upload your favorite songs, and our advanced algorithms will split the vocals and instrumentals, 
        allowing you to sing along with just the music while displaying the lyrics on screen.
    </p>
    <p class="text-lg leading-relaxed mt-4">
        Perfect for karaoke nights, parties, or just singing your heart out at home, KaraokeKit makes karaoke accessible and fun for everyone!
    </p>
    <div class="mt-8">
        <button
            class="bg-yellow-300 text-purple-800 font-bold py-2 px-6 rounded-full shadow-md hover:bg-yellow-400 transition"
            on:click={() => goto('/')}
        >
            Get Started
        </button>
    </div>
</div>