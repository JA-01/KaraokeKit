from flask import *
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return Response("Hello World")

@app.route('/process', methods=['POST'])
def process():
    
    file = request.files['file']
    print(os.getcwd() + "/static/uploads/" + file.filename)
    file.save(os.getcwd() + "/static/uploads/" + file.filename)

    

    response = jsonify({
            "lyrics": "Never gonna give you up",
            "audio": file.filename
        })
    
    response.data = file.read()

    response.headers['Content-Type'] = 'audio/mpeg'
    response.headers['Content-Disposition'] = f'attachment; filename="{file.filename}"'

    return response
    

if __name__ == '__main__':
    app.run(debug=True)