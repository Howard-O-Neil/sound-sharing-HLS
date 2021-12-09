import os
import uuid

parent_dir = os.getcwd()

def check_full_z(name):
    for character in name:
        if character != 'z': return False
    return True

def next_letter(s: str):
    if((s >= 'a' and s <= 'z') or (s >= 'A' and s <= 'Z')):
        return chr((ord(s.upper())+1 - 65) % 26 + 65).lower()
    else:
        raise Exception("Not an alphabet")

def next_string(s: str):
    print(s)
    s = list(s.lower())
    reverse_s = list(reversed(s))
    flag = False
    if check_full_z(s):
        return "a" * (len(s) + 1)

    for  idx in range(len(reverse_s)):
        char = reverse_s[idx]
        i = len(s) - (idx + 1) 
        next_char = next_letter(char)

        if char =='z': continue

        if next_char == 'z':
            s[i] = next_char
            flag = True
            break
        else:
            if i < len(s) - 1:
                s[i] = next_char
                return "".join(s[:(i + 1)]) + ("a" * (len(s) - 1 - i))
            else: 
                # print("fuck")
                # print(char)
                # print(next_char)
                s[i] = next_char
                flag = True
                break
    
    if flag == False: # very end condition, in case algorithm get error
        return "a" * (len(s) + 1)
    return "".join(s)
                        

def get_newest_partition():
    print(next_letter("y"))
    print(next_string("zzzz"))
    # list_partition = sorted(os.listdir('./upload'))

    # if len(list_partition) <= 0:
    #     name = uuid.uuid4()
    #     i
    # latest_partition = list_partition[len(list_partition) - 1]
