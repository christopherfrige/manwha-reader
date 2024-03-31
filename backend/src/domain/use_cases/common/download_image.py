import requests
import os


class DownloadImageUseCase:
    def execute(self, local_dir: str, image_name: str, image_type: str, image_url: str):
        os.makedirs(local_dir, exist_ok=True)
        with open(f"{local_dir}/{image_name}.{image_type}", "wb") as image:
            image.write(requests.get(image_url).content)
