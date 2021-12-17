
from flask import Flask, render_template, request, send_from_directory
from pprint import pprint
import partition
import media

import signal
import requests
import random
import string
import json
import os
import subprocess

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__)) # get parent of this folder

load_dotenv(os.path.join(BASEDIR, "development.env"))

CDN_DIR = os.getenv("CDN_DIR")
STREAM_SERVER = os.getenv("STREAM_SERVER")
PATH_REPLACE_STRING = os.getenv("PATH_REPLACE_STR")
DOT_REPLACE_STRING = os.getenv("DOT_REPLACE_STR")

stream_process = {}

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for _ in range(y))

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Sound Sharing CDN"

@app.route("/serve", methods=["GET"])
def serve_static():
    file_id = request.args.get("file-id")
    return send_from_directory(CDN_DIR, file_id)

@app.route("/start-stream-loop", methods=["GET"])
def start_content_stream():
    file_id = request.args.get("file-id")

    if file_id not in stream_process:
        stream_process[file_id] = {
            1: None,
            2: None,
        }
        stream_process[file_id][1] = media.ffmpeg_stream_loop(CDN_DIR, file_id, PATH_REPLACE_STRING, DOT_REPLACE_STRING)
        stream_process[file_id][2] = file_id.replace("/", PATH_REPLACE_STRING).replace(".", DOT_REPLACE_STRING)

        return json.dumps({
            "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[file_id][2]}.m3u8",
            "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[file_id][2]}.mpd",
            "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[file_id][2]}"
        })
    else:
        print("===============================")
        print(stream_process[file_id][1].pid)
        return json.dumps({
                "error": 400,
                "message": "stream already served",
                "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[file_id][2]}.m3u8",
                "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[file_id][2]}.mpd",
                "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[file_id][2]}"
        })

@app.route("/end-stream-loop", methods=["GET"])
def end_content_stream():
    file_id = request.args.get("file-id")

    if file_id in stream_process:
        os_kill = subprocess.run(["pkill", "-P", f"{stream_process[file_id][1].pid}"])

        stream_process.pop(file_id)

        return json.dumps({
            "os_kill_code": os_kill.returncode,
            # "sub_process_kill": sub_process_kill
        }) 
        
    return json.dumps({
        "error": 500,
        "message": "IDK what happen too :)))"
    })

@app.route("/create-stream", methods=["GET", "POST"])
def create_content_stream():
    file_id = request.args.get("file-id")

    res = requests.get(f"http://{STREAM_SERVER}:5001/check-available-stream?file-id={file_id}")
    
    print("===================")

    respose = json.loads(res._content.decode('utf-8'))
    stream_id = file_id.replace("/", PATH_REPLACE_STRING).replace(".", DOT_REPLACE_STRING)

    if respose["status"] == True:
        return json.dumps({
            "error": 400,
            "message": "create already exists",
            "stream-url-1": f"http://{STREAM_SERVER}/hls/{stream_id}.m3u8",
            "stream-url-2": f"http://{STREAM_SERVER}/hls/{stream_id}-X-ENDLIST.m3u8",
        })
    else:
        update_play_list_url = f"http://{STREAM_SERVER}:5001/create-x-endlist"
        _ = media.ffmpeg_create_stream_playlist(CDN_DIR, file_id, PATH_REPLACE_STRING, DOT_REPLACE_STRING, update_play_list_url)
        stream_id = stream_id + ".m3u8"
        
        return json.dumps({
            "stream-id-1": stream_id,
            "stream-id-2": stream_id.rsplit(".", 1)[0] + "-X-ENDLIST.m3u8",
        })

    # return "fuck"


    # return json.dumps({
    #     "sound-id": file_id,
    #     "stream-id": stream_id
    # })

    # if sound_id not in stream_process:
    #     stream_process[sound_id] = {
    #         1: None,
    #         2: None,
    #     }

    #     return json.dumps({
    #         "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[sound_id][2]}.m3u8",
    #         "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[sound_id][2]}.mpd",
    #         "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[sound_id][2]}"
    #     })
    # else:
    #     print("===============================")
    #     print(stream_process[sound_id][1].pid)
    #     return json.dumps({
    #             "error": 400,
    #             "message": "stream already served",
    #             "hls-url": f"http://{STREAM_SERVER}/hls/{stream_process[sound_id][2]}.m3u8",
    #             "dash-url":  f"http://{STREAM_SERVER}/dash/{stream_process[sound_id][2]}.mpd",
    #             "rtmp-url": f"rtmp://{STREAM_SERVER}:1935/show/{stream_process[sound_id][2]}"
    #     })


@app.route("/file-uploader", methods=["GET"])
def upload_file_template():
    return render_template("upload.html")


@app.route("/upload-file", methods=["POST"])
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

    return json.dumps(media.get_wav(CDN_DIR, os.path.join(CDN_DIR, sound_id)))


if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
