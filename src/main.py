
from flask import Flask, render_template, request, send_from_directory
import partition
import sound

import json
import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__)) # get parent of this folder

load_dotenv(os.path.join(BASEDIR, "development.env"))

CDN_DIR = os.getenv("CDN_DIR")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Sound Sharing HLS Server"

@app.route("/serve", methods=["GET"])
def serve_static():
    file_id = request.args.get("file-id")
    return send_from_directory(CDN_DIR, file_id)

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
