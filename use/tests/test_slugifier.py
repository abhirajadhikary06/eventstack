from use.shareable_links.slugifier import slugify

def test_basic_slug():
    assert slugify("Hackathon Kickoff!") == "hackathon-kickoff"

def test_with_special_chars():
    assert slugify("Dev@Meet#2025") == "devmeet2025"

def test_with_spaces_and_case():
    assert slugify("Open Source Summit") == "open-source-summit"