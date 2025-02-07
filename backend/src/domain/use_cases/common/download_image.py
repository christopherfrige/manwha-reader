import os

import requests


class DownloadImageUseCase:
    def __init__(self, referer: str | None):
        self.headers = {}
        if referer:
            self.headers = {
                "referer": referer,
            }

    def execute(self, local_dir: str, image_name: str, image_type: str, image_url: str):
        os.makedirs(local_dir, exist_ok=True)
        with open(f"{local_dir}/{image_name}.{image_type}", "wb") as image:
            image.write(self._get_image_content(image_url))

    def _get_image_content(self, image_url: str) -> bytes:
        return requests.get(image_url, headers=self.headers).content
