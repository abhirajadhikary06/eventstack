from use.shareable_links.link_generator import create_shareable_link

def test_link_contains_slug():
    event_name = "Dev Meet 2025"
    link = create_shareable_link(event_name)
    assert "dev-meet-2025" in link

def test_link_format_valid():
    event_name = "Demo Day"
    link = create_shareable_link(event_name)
    assert link.startswith("https://eventstack.onrender.com/event/")
    assert "-" in link.split("/")[-1]  # Ensures slug-ID separator