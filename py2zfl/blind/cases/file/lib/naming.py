"""Name normalisation used when turning user supplied titles into file names."""
import re

_SLUG_RE = re.compile(r"[^a-z0-9_-]+")


def clean_name(name):
    """Trim whitespace and lower-case a user supplied name."""
    return " ".join(name.split()).lower()


def slugify_name(name):
    """Reduce ``name`` to lowercase letters, digits, underscore and dash."""
    slug = _SLUG_RE.sub("-", name.lower()).strip("-")
    return slug or "untitled"
