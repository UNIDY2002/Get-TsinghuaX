import os
from os.path import join


def save(path: str, walk_id: int, name: str, data: str):
    if not os.path.exists(path):
        os.makedirs(path)
    file = open("%s/%03d. %s.txt" % (path, walk_id, name), 'w')
    file.write(data)
    file.close()


def search(path: str, s: str, on_success, on_error):
    for root, dirs, files in os.walk(path):
        for filename in files:
            try:
                file = open(join(root, filename))
                for line in file:
                    if s in line:
                        on_success(root, filename, line)
            except Exception as e:
                on_error(root, filename, e)
