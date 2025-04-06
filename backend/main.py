from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
from dotenv import load_dotenv
from io import BytesIO, StringIO
import requests
from elevenlabs.client import ElevenLabs
import re
import time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()
client = ElevenLabs(
    api_key="sk_8a9b175e93f1690b86df18ddcf1e45632b65578c74aafbc1"
)
TIME_BETWEEN_SENTENCES = 3  # seconds

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
    
    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    audio_data_io = BytesIO(audio_data)
    
    # Reset pointer to beginning of file
    audio_data_io.seek(0)
    
    transcription = client.speech_to_text.convert(
        file=audio_data_io,
        model_id="scribe_v1",
        language_code="eng",
    )
    
    # Convert the transcription text to SRT format
    srt_content = convert_to_srt(transcription.text)
    
    # Create a file-like object from the SRT content
    srt_io = BytesIO(srt_content.encode('utf-8'))

    return send_file(
        srt_io,
        mimetype='text/plain', 
        as_attachment=True,
        download_name=f"{text.split('.')[0]}.srt"
    )   

def convert_to_srt(transcription_text):
    """Convert plain text to SRT format with timestamps."""
    # Split text into sentences or phrases
    sentences = re.split(r'(?<=[.!?])\s+', transcription_text.strip())
    
    srt_content = ""
    for i, sentence in enumerate(sentences, 1):
            
        # Calculate simple timestamps (this is simplified)
        # In reality, you'd want more accurate timestamps from a proper transcription service
        start_time = (i - 1) * TIME_BETWEEN_SENTENCES 
        end_time = i * TIME_BETWEEN_SENTENCES
        
        # Format timestamps as HH:MM:SS,mmm
        start_formatted = format_timestamp(start_time)
        end_formatted = format_timestamp(end_time)
        
        # Add to SRT content
        srt_content += f"{i}\n{start_formatted} --> {end_formatted}\n{sentence}\n\n"
    
    return srt_content

def format_timestamp(seconds):
    """Format seconds to HH:MM:SS,mmm format."""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

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