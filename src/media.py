import json
import subprocess
import uuid
import os
import random
import string
import partition
import threading
import requests

this_dir = os.getcwd()

wav_form_color = "0EAE59"


def get_wav(parent_dir, full_file_dir: str, width=600, height=120):

    out_file_name = (
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp/")
        + str(uuid.uuid4())
        + ".png"
    )
    bash_cmd = f"""
        ffmpeg -i {full_file_dir} \
            -filter_complex \
                "[0:a]aformat=channel_layouts=mono, \
                compand=gain=-6, \
                showwavespic=s={width}x{height}:colors=#{wav_form_color}[fg]; \
                color=s={width}x{height}:color=#FFFFFF@0.0, \
                drawgrid=width=iw/10:height=ih/5:color=#FFFFFF@0.0[bg]; \
                [bg][fg]overlay=format=auto,drawbox=x=(iw-w)/2:y=(ih-h)/2:w=iw:h=1:color=#{wav_form_color}" \
            -frames:v 1 {out_file_name}
    """
    bash_cmd = bash_cmd.strip()
    # print("===================")
    # print(bash_cmd)

    process = subprocess.Popen(
        bash_cmd, bufsize=2048, stdout=subprocess.PIPE, shell=True
    )
    process.wait()

    if process.returncode == 0:
        return partition.move_file(parent_dir, out_file_name)
    return {"error": 500, "message": "IDK what happen too :)))"}


def random_char(y):
    return "".join(random.choice(string.ascii_letters) for _ in range(y))


def ffmpeg_stream_loop(parent_dir: str, sound_id: str, replace_path_str: str, replace_dot_str: str):
    sound_file = os.path.join(parent_dir, sound_id)

    bash_cmd = f"""
        ffmpeg -re -stream_loop -1 \
            -i {sound_file} \
            -vcodec copy -preset ultrafast -c:a aac -b:a 160k -ar 44100 \
            -strict -2 -f flv rtmp://128.0.3.2:1935/show/{sound_id.replace("/", replace_path_str).replace(".", replace_dot_str)}
    """
    bash_cmd = bash_cmd.strip()

    process = subprocess.Popen(
        bash_cmd, bufsize=2048, stdout=subprocess.PIPE, shell=True
    )
    return process


def ffmpeg_create_stream_playlist(
    parent_dir: str,
    sound_id: str,
    replace_path_str: str,
    replace_dot_str: str,
    update_play_list_url: str,
):
    sound_file = os.path.join(parent_dir, sound_id)

    def run_bash(onExit):
        bash_cmd = f"""
            ffmpeg -re \
            -i {sound_file} \
            -vcodec copy -preset ultrafast -c:a aac -b:a 160k -ar 44100 \
            -strict -2 -f flv rtmp://128.0.3.2:1935/show/{sound_id.replace("/", replace_path_str).replace(".", replace_dot_str)}
        """
        bash_cmd = bash_cmd.strip()

        process = subprocess.Popen(
            bash_cmd, bufsize=2048, stdout=subprocess.PIPE, shell=True
        )
        process.wait()
        onExit()

    def update_playlist():
        post_obj = {"stream-id": sound_id.replace("/", replace_path_str).replace(".", replace_dot_str)}

        requests.post(update_play_list_url, json=post_obj)

    thread = threading.Thread(target=run_bash, args=(update_playlist,))
    thread.start()

    return thread
