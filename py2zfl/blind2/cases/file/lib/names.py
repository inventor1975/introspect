import os
import re

_ALLOWED = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


class InvalidName(ValueError):
    pass


def clean_name(raw):
    """Reduce a client-supplied name to a single, plain file name."""
    if raw is None:
        raise InvalidName("missing")
    candidate = os.path.basename(raw.replace("\\", "/"))
    if candidate in ("", ".", ".."):
        raise InvalidName("empty")
    if not _ALLOWED.fullmatch(candidate):
        raise InvalidName("characters")
    return candidate


def normalize_strict(raw):
    """Reject anything that is not already a plain name."""
    if "/" in raw or "\\" in raw or raw.startswith("."):
        raise InvalidName(raw)
    return raw
