import os
import uuid
import shutil
from typing import List
from functools import cmp_to_key
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

FILE_EACH_PARTITION = 3

def check_full_z(name):
    for character in name:
        if character != "z":
            return False
    return True


def next_letter(s: str):
    if (s >= "a" and s <= "z") or (s >= "A" and s <= "Z"):
        return chr((ord(s.upper()) + 1 - 65) % 26 + 65).lower()
    else:
        raise Exception("Not an alphabet")

def check_alphabet_path(s: str):
    s = list(s.lower())

    for char in s:
        if (char >= "a" and char <= "z") or (char >= "A" and char <= "Z"):
            continue
        else:
            return False
    return True

def get_latest_partition(l: List[str]):
    if not check_alphabet_path(l[-1]):
        return None
    return l[-1]

def next_string(s: str):
    s = list(s.lower())

    reverse_s = list(reversed(s))
    flag = False

    if check_full_z(s):
        return "a" * (len(s) + 1)

    for idx in range(len(reverse_s)):
        char = reverse_s[idx]
        i = len(s) - (idx + 1)

        if char == "z":
            continue
        
        next_char = next_letter(char)

        if i < len(s) - 1:
            s[i] = next_char
            return "".join(s[: (i + 1)]) + ("a" * (len(s) - 1 - i))
        else:
            s[i] = next_char
            flag = True
            break

    if flag == False:  # very end condition, in case algorithm get error
        return "a" * (len(s) + 1)
    return "".join(s)


def mkdir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def compare_path(item1: str, item2: str):
    return_value = 1

    if len(item1) > len(item2):
        return_value = 1
    elif len(item1) < len(item2):
        return_value = -1
    else:
        if item1 > item2:
            return_value = 1
        elif item1 < item2:
            return_value = -1
        else:
            return_value = 0

    return return_value


def save_file(parent_dir, file: FileStorage):
    list_partition = sorted(
        os.listdir(parent_dir), key=cmp_to_key(compare_path)
    )  # list level1 + sorted
    partition = ""

    if len(list_partition) == 0:
        partition = "a"
        mkdir(os.path.join(parent_dir, partition))
    elif len(list_partition) > 0:
        partition = get_latest_partition(list_partition)

    if partition == None:
        partition = "a" * (len(list_partition[-1]) + 1)
        mkdir(os.path.join(parent_dir, partition))
    
    if len(os.listdir(os.path.join(parent_dir, partition))) >= FILE_EACH_PARTITION:
        partition = next_string(partition)
        mkdir(os.path.join(parent_dir, partition))

    secure_f = secure_filename(file.filename)
    extension = secure_f.rsplit(".", 1)[1]
    secure_f = os.path.join(
        os.path.join(parent_dir, partition),
        f"{secure_f.rsplit('.', 1)[0]}-{str(uuid.uuid4())}.{extension}",
    )

    file.save(secure_f)

    return {
        "filename": os.path.join(
            partition, os.path.basename(os.path.normpath(secure_f))
        ),
        "size": os.stat(secure_f).st_size,
        "size_measure": "bytes",
    }


def move_file(parent_dir, full_file_dir):
    list_partition = sorted(
        os.listdir(parent_dir), key=cmp_to_key(compare_path)
    )  # list level1 + sorted
    partition = ""

    if len(list_partition) == 0:
        partition = "a"
        mkdir(os.path.join(parent_dir, partition))
    elif len(list_partition) > 0:
        partition = get_latest_partition(list_partition)

    if len(os.listdir(os.path.join(parent_dir, partition))) >= FILE_EACH_PARTITION:
        partition = next_string(partition)
        mkdir(os.path.join(parent_dir, partition))

    secure_f = secure_filename(os.path.basename(os.path.normpath(full_file_dir)))
    extension = secure_f.rsplit(".", 1)[1]
    secure_f = os.path.join(
        os.path.join(parent_dir, partition),
        f"{secure_f.rsplit('.', 1)[0]}-{str(uuid.uuid4())}.{extension}",
    )

    shutil.copy(full_file_dir, secure_f)
    
    if os.path.exists(full_file_dir):
        os.remove(full_file_dir)

    return {
        "filename": os.path.join(
            partition, os.path.basename(os.path.normpath(secure_f))
        ),
        "size": os.stat(secure_f).st_size,
        "size_measure": "bytes",
    }
