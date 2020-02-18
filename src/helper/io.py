import os


def save(path: str, walk_id: int, name: str, data: str):
    if not os.path.exists(path):
        os.makedirs(path)
    file = open("%s/%03d. %s.txt" % (path, walk_id, name), 'w')
    file.write(data)
    file.close()
