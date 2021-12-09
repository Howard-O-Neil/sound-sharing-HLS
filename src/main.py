
from flask import Flask, render_template, request
import partition
import sound

import json
import os

from dotenv import load_dotenv

def loadEnv():
    environPath = None

    flask_env = os.environ.get("FLASK_ENV")
    environPath = f"{'development' if flask_env is None else flask_env}.env"

    load_dotenv(environPath)


loadEnv()

SOUND_DIR = os.environ.get("SOUND_DIR")
CDN_DIR = os.environ.get("CDN_DIR")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return "Sound Sharing HLS Server"


@app.route("/sound-uploader", methods=["GET"])
def upload_file_template():
    return render_template("upload.html")


@app.route("/upload-sound", methods=["POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]

        if (f.filename.rsplit('.', 1)[1].lower() == 'wav' or
            f.filename.rsplit('.', 1)[1].lower() == 'mp3' or
            f.filename.rsplit('.', 1)[1].lower() == 'm4a'):

            return json.dumps(partition.save_file(SOUND_DIR, f))
        else:
            f.close()
            return json.dumps({
                    "error": 400,
                    "message": "file extension not supported"
                })

@app.route("/extract-wav-img", methods=["GET"])
def extract_wav_img():
    sound_id = request.args.get("sound-id")

    return json.dumps(sound.get_wav(CDN_DIR, os.path.join(SOUND_DIR, sound_id)))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
