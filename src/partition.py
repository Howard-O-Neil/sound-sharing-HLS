import os
import uuid
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

FILE_EACH_PARTITION = 3
parent_dir = os.path.join(os.getcwd(), "upload")


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


def next_string(s: str):
    s = list(s.lower())

    for char in s:
        if (char >= "a" and char <= "z") or (char >= "A" and char <= "Z"):
            continue
        else:
            raise Exception("Not an alphabet")

    reverse_s = list(reversed(s))
    flag = False

    if check_full_z(s):
        return "a" * (len(s) + 1)

    for idx in range(len(reverse_s)):
        char = reverse_s[idx]
        i = len(s) - (idx + 1)
        next_char = next_letter(char)

        if char == "z":
            continue

        if next_char == "z":
            s[i] = next_char
            flag = True
            break
        else:
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


def save_file(file: FileStorage):
    list_partition = sorted(os.listdir(parent_dir))  # list level1 + sorted
    partition = ""

    if len(list_partition) == 0:
        partition = "a"
        os.mkdir(os.path.join(parent_dir, partition))
    elif len(list_partition) > 0:
        partition = list_partition[len(list_partition) - 1]

    if len(os.listdir(os.path.join(parent_dir, partition))) >= FILE_EACH_PARTITION:
        partition = next_string(partition)
        os.mkdir(os.path.join(parent_dir, partition))

    secure_f = secure_filename(file.filename)
    extension = secure_f.rsplit(".", 1)[1]
    secure_f = os.path.join(
        os.path.join(parent_dir, partition), str(uuid.uuid4()) + "." + extension
    )

    file.save(secure_f)

    return {
        "filename": secure_f,
        "size": os.stat(secure_f).st_size,
        "size_measure": "bytes",
    }
