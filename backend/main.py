from flask import *
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), "processed"), exist_ok=True)

@app.route('/helloworld', methods=['GET'])
@cross_origin()
def helloworld():
    return Response("Hello World")

@app.route('/process', methods=['POST'])
@cross_origin()
def process():
    
    file = request.files['file']
    print(os.getcwd() + "/static/uploads/" + file.filename)
    file.save(os.getcwd() + "/static/uploads/" + file.filename)

    #os.mkdir(os.getcwd() + "/processed/" file.filename.split('.')[0])


    response = jsonify({
            "lyrics": "Never gonna give you up",
            "audio": file.filename
        })
    
    response.data = file.read()

    response.headers['Content-Type'] = 'audio/mp3'
    response.headers['Content-Disposition'] = f'attachment; filename="{file.filename}"'

    return response
    

if __name__ == '__main__':
    app.run(debug=True)