import requests

from src.domain.utils import normalize_string
from src.domain.entities.manwha import Manwha
from src.infrastructure.config import SETTINGS


class Notifier:
    @staticmethod
    def notify_discord(manwha: Manwha, chapter_number: int):
        payload = {
            "embeds": [
                {
                    "title": manwha.name,
                    "url": f"{SETTINGS.manwha_reader_url}/manwha/{normalize_string(manwha.name)}?id={manwha.id}",
                    "fields": [{"name": f"Capítulo {chapter_number}", "value": ""}],
                    "thumbnail": {"url": manwha.thumbnail},
                }
            ]
        }
        requests.post(SETTINGS.discord_webhook_url, json=payload)
