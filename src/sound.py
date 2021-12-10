import subprocess
import uuid
import os

import partition

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
    print("===================")
    print(bash_cmd)

    process = subprocess.Popen(
        bash_cmd, bufsize=2048, stdout=subprocess.PIPE, shell=True
    )
    process.wait()

    if process.returncode == 0:
        return partition.move_file(parent_dir, out_file_name)
    return {"error": 500, "message": "IDK what happen too :)))"}
