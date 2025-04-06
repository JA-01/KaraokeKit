<script lang="ts">
    import { onMount } from "svelte";

    let isDarkMode = false;

    onMount(() => {
        isDarkMode = document.documentElement.classList.contains("dark");

        const observer = new MutationObserver(() => {
            isDarkMode = document.documentElement.classList.contains("dark");
        });
        observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
        return () => observer.disconnect();
    });
</script>

<div
    class={`bg-white bg-opacity-10 backdrop-blur-md rounded-lg shadow-lg p-8 max-w-3xl text-center ${
        isDarkMode ? "text-white" : "text-black"
    }`}
>
    <h1 class="text-5xl font-extrabold mb-6 drop-shadow-lg">
        How to Use KaraokeKit
    </h1>
    <ol class="mt-4 text-lg leading-relaxed list-decimal list-inside">
        <li>Upload your audio file using the upload button on the homepage. Supported formats include MP3, WAV, and OGG.</li>
        <li>Or, paste a YouTube link in the YouTube Generator tab to process the video.</li>
        <li>Wait for the processing to complete. KaraokeKit uses advanced audio processing algorithms to separate the vocals and instrumentals of the song.</li>
        <li>Once processing is complete, KaraokeKit allows you to play back the instrumental track while displaying the lyrics on screen.</li>
        <li>Grab your microphone (or just sing out loud) and enjoy karaoke with any song you love!</li>
    </ol>
    <p class="text-lg leading-relaxed mt-4">
        KaraokeKit makes it easy to enjoy karaoke with your favorite songs. Follow these steps and start singing!
    </p>
</div>