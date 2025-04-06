from flask import *
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
import whisper
from whisper.utils import get_writer

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()

model = whisper.load_model()

@app.route('/helloworld', methods=['GET'])
@cross_origin()
def helloworld():
    return Response("Hello World")

@app.route('/lyrics', methods=['POST'])
@cross_origin()
def lyrics():
    data = request.get_json()
    text = data['text']

    audiofile = os.path.join(os.getcwd(), "static", text.split('.')[0], text)
    if not os.path.isfile(audiofile):
        return abort(404, description="File not found")
    result = model.transcribe(audiofile, word_timestamps=True)

    output_directory = os.path.join(os.getcwd(), "static", text.split('.')[0])
    writer = get_writer("srt", output_directory)
    writer(result, output_directory)

    return send_file(
        os.path.join(output_directory),
        mimetype='text/plain', 
        as_attachment=True,
        download_name="srtfile"
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