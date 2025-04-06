from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
from io import BytesIO
import requests
import whisper
import time
import yt_dlp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()

whisper_model = whisper.load_model("small.en")

@app.route('/ytdl', methods=['GET'])
@cross_origin
def yt_splitter():
    data = request.get_json()
    url = data.get('url')
    save_path = yt_download(url)

    outputfolder = os.path.join(os.getcwd(), "static", url.split('=')[-1])

    custom_output_names = {
        "vocals": os.path.join(outputfolder, "vocals"),
        "instrumental": os.path.join(outputfolder, "instrumental")
    }
    separator.separate(save_path, custom_output_names)
    return send_file(
        custom_output_names["instrumental"] + ".wav",
        mimetype='audio/wav',
        as_attachment=True,
        download_name="ytdl.wav"
    )



def yt_download(url):
    # Create static folder if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')

    # Use a safe filename from URL (you can improve this if needed)
    url_name = url.split('=')[-1]  # Get the video ID
    output_path = os.path.join(os.getcwd(), 'static', url_name, url_name + ".mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,  # Save to static/urlname.mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        final_path = os.path.join(os.getcwd(), 'static', f"{url_name}.mp3")
        return final_path  # Return the path of the downloaded file
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")

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