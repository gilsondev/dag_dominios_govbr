import requests

from pathlib import Path


class DownloadFileProcessor:
    def __init__(self, url: str, filename: str, path: str):
        self.url = url
        self.filename = filename
        self.path = path

    def _download(self):
        destination_path = f'{self.path}/{self.filename}'
        response = requests.get(self.url, stream=True)

        with open(Path(destination_path), 'w') as file:
            file.write(response.text)

    def run(self):
        self._download()
