import re

def slugify(event_name: str) -> str:
    slug = event_name.lower()
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'[^\w\-]', '', slug)
    return slug