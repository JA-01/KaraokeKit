from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
from dotenv import load_dotenv
from io import BytesIO, StringIO
import requests
from elevenlabs.client import ElevenLabs
import whisper
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()

whisper_model = whisper.load_model("small.en")

@app.route('/helloworld', methods=['GET'])
@cross_origin()
def helloworld():
    return Response("Hello World")


@app.route('/lyrics', methods=['POST'])
@cross_origin()
def lyrics():
    data = request.get_json()
    text = data['text']
    audio_path = os.path.join(os.getcwd(), "static", text.split('.')[0], "vocals.wav")
    
    result = whisper_model.transcribe(audio_path, task="transcribe")
    srt_content = generate_srt(result['segments'])
    srt_io = BytesIO(srt_content.encode('utf-8'))

    return send_file(
        srt_io,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"{text.split('.')[0]}.srt"
    )


def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    time_str = time.strftime('%H:%M:%S', time.gmtime(seconds))
    return f"{time_str},{milliseconds:03d}"

def generate_srt(segments):
    srt = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment['start'])
        end = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt

@app.route('/process', methods=['POST'])
@cross_origin()
def process():
    file = request.files['file']
    filename = file.filename.split('.')[0]
    outputfolder = os.path.join(os.getcwd(), "static", filename)
    os.makedirs(outputfolder, exist_ok=True)
    save_path = os.path.join(os.getcwd(), "static", filename, file.filename)
    file.save(save_path)
    custom_output_names = {
        "vocals": os.path.join(outputfolder, "vocals"),
        "instrumental": os.path.join(outputfolder, "instrumental")
    }
    separator.separate(save_path, custom_output_names)
    return send_file(
        custom_output_names["instrumental"] + ".wav",
        mimetype='audio/wav',
        as_attachment=True,
        download_name=file.filename
    )
    
if __name__ == '__main__':
    app.run(debug=True)