"""
This script used only in stream server
Open endpoint to handle some stream file
"""


from pprint import pprint
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

import json
import os
from glob import glob

app = Flask(__name__)

PATH_REPLACE_STRING = "FmlZZ3ruyNP5Yr9LfnNS"
DOT_REPLACE_STR = "sd1gNq6C2B"

@app.route("/", methods=["GET"])
def hello():
    return "Sound Sharing HLS server"

@app.route("/check-available-stream", methods=["GET"])
def check_stream():
    stream_id = request.args.get("file-id").replace("/", PATH_REPLACE_STRING).replace(".", DOT_REPLACE_STR)

    return json.dumps({
        "status": len(glob(f"/home/root/stream/hls/{stream_id}*")) > 0
    })

@app.route("/create-x-endlist", methods=["POST"])
def create_x_endlist():

    stream_id = request.json["stream-id"]

    # filename = os.listdir(os.)
    filename = glob(f"/home/root/stream/hls/*{stream_id}.m3u8")[0]

    playlist_content = ""
     
    original_f = os.open(filename, os.O_RDONLY)
    playlist_content = os.read(original_f, os.path.getsize(filename) * 2).decode('utf-8')
    playlist_content += "#EXT-X-ENDLIST\r\n"
    os.close(original_f)

    f = os.open(f"/home/root/stream/hls/{stream_id}-X-ENDLIST.m3u8", os.O_CREAT | os.O_WRONLY)
    os.write(f, playlist_content.encode('utf-8'))
    os.close(f)

    return json.dumps({
        "playlist-id": f"/home/root/stream/hls/{stream_id}-X-ENDLIST.m3u8"
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
