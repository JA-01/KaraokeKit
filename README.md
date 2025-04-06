# KaraokeKit

KaraokeKit is a powerful and easy-to-use platform that transforms any song into a karaoke track. With KaraokeKit, you can upload your favorite songs, and our advanced algorithms will split the vocals and instrumentals, allowing you to sing along with just the music while displaying the lyrics on screen. Perfect for karaoke nights, parties, or just singing your heart out at home!

---

## Features

- **Vocal and Instrumental Separation**  
  Upload any song, and KaraokeKit will automatically split the vocals and instrumentals for you.

- **Lyrics Display**  
  Watch the lyrics appear on screen in sync with the music, making it easy to follow along.

- **Karaoke-Ready Playback**  
  Enjoy seamless playback of the instrumental track while performing karaoke.

- **Web-Based Platform**  
  No downloads required — use KaraokeKit directly in your browser.

---

## How It Works

1. **Upload Your Song**  
   Drag and drop your audio file or click to upload. Supported formats include MP3 and WAV.

2. **Processing**  
   KaraokeKit uses advanced audio processing algorithms to separate the vocals and instrumentals of the song.

3. **Playback and Lyrics**  
   Once processing is complete, KaraokeKit plays back the instrumental track while displaying the lyrics on screen.

4. **Sing Along!**  
   Grab your microphone (or just sing out loud) and enjoy karaoke with any song you love.

---

## Project Structure

### Frontend
- **Framework**: Built with [SvelteKit](https://kit.svelte.dev/) for a fast and responsive user interface.
- **Features**:
  - Drag-and-drop file upload.
  - YouTube link processing.
  - Real-time lyrics synchronization.
  - Audio playback with a sleek UI.
  - Light/Dark mode toggle.

### Backend
- **Framework**: Built with [Flask](https://flask.palletsprojects.com/) for handling API requests.
- **Features**:
  - Separates vocals and instrumentals using the `audio-separator` library.
  - Transcribes lyrics using OpenAI's `whisper` model.
  - Processes YouTube links and extracts audio.
  - Returns instrumental tracks and synchronized lyrics.
