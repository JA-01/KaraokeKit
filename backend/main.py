from flask import Flask, request, Response, send_file
from flask_cors import CORS, cross_origin
import os
from audio_separator.separator import Separator
from io import BytesIO
from faster_whisper import WhisperModel
import time
import yt_dlp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

separator = Separator()
separator.load_model()

# Initialize faster-whisper model
whisper_model = WhisperModel("small", device="cuda", compute_type="float16")

@app.route('/ytdl', methods=['POST'])
@cross_origin()
def yt_splitter():
    data = request.get_json()
    url = data.get('url')
    save_path = yt_download(url)

    # use the YouTube video ID as folder name
    video_id = url.split('=')[-1]
    outputfolder = os.path.join(os.getcwd(), "static", video_id)
    os.makedirs(outputfolder, exist_ok=True)

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
    if not os.path.exists('static'):
        os.makedirs('static')

    video_id = url.split('=')[-1]  # video ID
    output_dir = os.path.join(os.getcwd(), 'static', video_id)
    os.makedirs(output_dir, exist_ok=True)

    output_template = os.path.join(output_dir, video_id)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template + '.%(ext)s',  # Important: add .%(ext)s
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Because you are converting to mp3, predict mp3 filename
        return output_template + '.mp3'
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
    print(data)
    # Now expect a "filename" key that matches the folder used during processing
    filename = data.get('text')
    print(filename)
    
    # Construct the path to the vocals file
    audio_path = os.path.join(os.getcwd(), "static", filename, "vocals.wav")
    
    
    # Using faster-whisper for transcription
    segments, info = whisper_model.transcribe(audio_path, task="transcribe")
    
    # Convert segments to list and generate SRT content
    segments_list = list(segments)
    srt_content = generate_srt(segments_list)
    srt_io = BytesIO(srt_content.encode('utf-8'))

    return send_file(
        srt_io,
        mimetype='text/plain',
        as_attachment=True,
        download_name=f"{filename}.srt"
    )

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    time_str = time.strftime('%H:%M:%S', time.gmtime(seconds))
    return f"{time_str},{milliseconds:03d}"

def generate_srt(segments):
    srt = ""
    for i, segment in enumerate(segments, start=1):
        start = format_timestamp(segment.start)
        end = format_timestamp(segment.end)
        text = segment.text.strip()
        srt += f"{i}\n{start} --> {end}\n{text}\n\n"
    return srt

@app.route('/process', methods=['POST'])
@cross_origin()
def process():
    file = request.files['file']
    filename = file.filename.split('.')[0]
    outputfolder = os.path.join(os.getcwd(), "static", filename)
    os.makedirs(outputfolder, exist_ok=True)
    save_path = os.path.join(outputfolder, file.filename)
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
