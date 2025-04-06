from audio_separator.separator import Separator

separator = Separator()
separator.load_model()
output_files = separator.separate('audio.mp3')

print(f"Separation complete! Output file(s): {' '.join(output_files)}")