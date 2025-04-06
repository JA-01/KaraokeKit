import whisper
from whisper.utils import get_writer

model = whisper.load_model("base")
result = model.transcribe(r"C:\Users\Jasee\Stuff\KaraokeKit\static\audio\vocals.wav")

print(result)