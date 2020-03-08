import os
import re
from os.path import join


def save(path: str, walk_id: int, name: str, data: str):
    if not os.path.exists(path):
        os.makedirs(path)
    file = open("%s/%03d. %s.txt" % (path, walk_id, name), 'w', encoding='utf-8')
    file.write(data)
    file.close()


def search(path: str, s: str, on_success, on_error):
    if path == '':
        search_path = '.'
    else:
        search_path = path
    for root, dirs, files in os.walk(search_path):
        for filename in files:
            if re.match('^.*\\.txt$', filename):
                try:
                    file = open(join(root, filename), encoding='utf-8')
                    for line in file:
                        if s in line:
                            on_success(root, filename, line)
                except Exception as e:
                    on_error(root, filename, e)
