from flask import *
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()

@app.route('/helloworld', methods=['GET'])
@cross_origin()
def helloworld():
    return Response("Hello World")

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