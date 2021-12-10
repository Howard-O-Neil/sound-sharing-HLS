
from flask import Flask, render_template, request, send_from_directory
import partition
import sound

import signal
import json
import os
import subprocess

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__)) # get parent of this folder

load_dotenv(os.path.join(BASEDIR, "development.env"))

CDN_DIR = os.getenv("CDN_DIR")
STREAM_SERVER = os.getenv("STREAM_SERVER")

stream_process = {}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Sound Sharing HLS Server"

@app.route("/serve", methods=["GET"])
def serve_static():
    file_id = request.args.get("file-id")
    return send_from_directory(CDN_DIR, file_id)

@app.route("/start-stream", methods=["GET"])
def start_sound_stream():
    sound_id = request.args.get("sound-id")

    if sound_id not in stream_process:
        stream_process[sound_id] = {
            1: None,
            2: None,
        }
        stream_process[sound_id][1], random_str = sound.ffmpeg_stream(CDN_DIR, sound_id)
        stream_process[sound_id][2] = sound_id.replace("/", random_str)

        return json.dumps({
            "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[sound_id][2]}.m3u8",
            "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[sound_id][2]}.mpd",
            "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[sound_id][2]}"
        })
    else:
        print("===============================")
        print(stream_process[sound_id][1].pid)
        return json.dumps({
                "error": 400,
                "message": "stream already served",
                "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[sound_id][2]}.m3u8",
                "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[sound_id][2]}.mpd",
                "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[sound_id][2]}"
        })

@app.route("/end-stream", methods=["GET"])
def end_sound_stream():
    sound_id = request.args.get("sound-id")

    if sound_id in stream_process:
        os_kill = subprocess.run(["pkill", "-P", f"{stream_process[sound_id][1].pid}"])

        stream_process.pop(sound_id)

        return json.dumps({
            "os_kill_code": os_kill.returncode,
            # "sub_process_kill": sub_process_kill
        }) 
        
    return json.dumps({
        "error": 500,
        "message": "IDK what happen too :)))"
    })

@app.route("/sound-uploader", methods=["GET"])
def upload_file_template():
    return render_template("upload.html")


@app.route("/upload-sound", methods=["POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]

        if (f.filename.rsplit('.', 1)[1].lower() == 'wav' or
            f.filename.rsplit('.', 1)[1].lower() == 'mp3' or
            f.filename.rsplit('.', 1)[1].lower() == 'm4a' or
            f.filename.rsplit('.', 1)[1].lower() == 'mp4'):

            return json.dumps(partition.save_file(CDN_DIR, f))
        else:
            f.close()
            return json.dumps({
                    "error": 400,
                    "message": "file extension not supported"
                })

@app.route("/extract-wav-img", methods=["GET"])
def extract_wav_img():
    sound_id = request.args.get("sound-id")

    return json.dumps(sound.get_wav(CDN_DIR, os.path.join(CDN_DIR, sound_id)))


if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
