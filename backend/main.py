from flask import *
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
from dotenv import load_dotenv
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs

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

@app.route('/helloworld', methods=['GET'])
@cross_origin()
def helloworld():
    return Response("Hello World")

@app.route('/lyrics', methods=['POST'])
@cross_origin()
def lyrics():
    data = request.get_json()
    text = data['text']

    audio_path = os.path.join(os.getcwd(), "static", text.split('.')[0], text)

    with open(audio_path, 'rb') as audio_file:
        audio_data = audio_file.read()

    audio_data_io = BytesIO(audio_data)

    
    transcription = client.speech_to_text.convert(
        file=audio_data_io,
        model_id="scribe_v1",
        language_code="eng"
    )

    print(transcription.text)
    return send_file(
        transcription,
        mimetype='text/plain', 
        as_attachment=True,
        download_name=f"{text.split('.')[0]}.srt"
    )


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