import uuid
from .slugifier import slugify

def create_shareable_link(event_name: str) -> str:
    event_id = str(uuid.uuid4())[:8]  # Short UUID for brevity
    slug = slugify(event_name)
    base_url = "https://eventstack.onrender.com/event"
    return f"{base_url}/{slug}-{event_id}"