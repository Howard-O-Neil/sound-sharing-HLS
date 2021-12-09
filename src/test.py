from functools import cmp_to_key

arr = ["a", "z", "b", "aa"]
l = list(arr)

def compare(item1: str, item2: str):
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
        else: return_value = 0

    return return_value
    # return return_value * -1

l.sort(key=cmp_to_key(compare))
print(l)