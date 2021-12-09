
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from partition import save_file

import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "Sound Sharing HLS Server"


@app.route("/upload")
def upload_file_template():
    return render_template("upload.html")


@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]

        if (f.filename.rsplit('.', 1)[1].lower() == 'wav' or
            f.filename.rsplit('.', 1)[1].lower() == 'mp3' or
            f.filename.rsplit('.', 1)[1].lower() == 'm4a'):

            return json.dumps(save_file(f))
        else:
            f.close()
            return json.dumps({
                    "error": 400,
                    "message": "file extension not supported"
                })


if __name__ == "__main__":
    app.run(port=5001, debug=True)
