"""Text normalisation helpers for user-supplied profile fields."""
import re

_SCRIPT_BLOCK = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL)
_WS = re.compile(r"\s+")


def strip_script_tags(text):
    return _SCRIPT_BLOCK.sub("", text)


def collapse_ws(text):
    return _WS.sub(" ", text).strip()


def truncate(text, limit=280):
    return text if len(text) <= limit else text[: limit - 1] + "…"
