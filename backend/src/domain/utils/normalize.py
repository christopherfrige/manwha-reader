import re
import unicodedata


def normalize_string(input_str: str) -> str:
    normalized_str = unicodedata.normalize("NFD", input_str)
    normalized_str = re.sub(r"[\u0300-\u036f]", "", normalized_str)
    normalized_str = re.sub(r"[^\w\s]", "", normalized_str)
    normalized_str = re.sub(r"\s+", "-", normalized_str)
    return normalized_str.lower()
