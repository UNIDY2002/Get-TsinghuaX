import os

from helper.io import search


class Searcher:
    path = os.getcwd()

    def search(self, s: str, on_success, on_error):
        search(self.path, s, on_success, on_error)

    def cd(self, directory: str, on_success, on_error):
        try:
            os.chdir(directory)
            self.path = os.getcwd()
            on_success(self.path)
        except Exception as e:
            on_error(self.path, e)
