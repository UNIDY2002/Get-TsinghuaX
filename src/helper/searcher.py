import re
from os.path import join, exists

from helper.io import search


class Searcher:
    path = ''

    def search(self, s: str, on_success, on_error):
        search(self.path, s, on_success, on_error)

    def cd(self, directory: str) -> bool:
        directory = directory.strip()
        path = self.path
        if directory == '.':
            pass
        elif directory == '..':
            match = re.search('[/\\\\]', self.path[::-1])
            if match:
                path = self.path[:-match.start() - 1]
        else:
            if directory.endswith(('/', '\\')):
                directory = directory[:-1]
            if directory.startswith(('/', '\\')):
                path = directory
            elif self.path == '':
                path = '/' + directory
            elif directory.strip() != '':
                path = join(self.path, directory)
        if exists(path) or path == '':
            self.path = path
            return True
        else:
            return False
