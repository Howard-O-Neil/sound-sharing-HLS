import subprocess
import uuid
import os

import partition

this_dir = os.getcwd()


def get_wav(parent_dir, full_file_dir: str):

    out_file_name = "temp/" + str(uuid.uuid4()) + ".png"

    bash_cmd = f"""
        ffmpeg -i {full_file_dir} \
            -filter_complex compand,showwavespic=s=640x120 \
            -frames:v 1 {out_file_name}
    """
    bash_cmd = bash_cmd.strip()
    process = subprocess.Popen(bash_cmd.split(), bufsize=2048, stdout=subprocess.PIPE)
    process.wait()

    if process.returncode == 0:
        return partition.move_file(parent_dir, out_file_name)
    return {"error": 500, "message": "IDK what happen too :)))"}
