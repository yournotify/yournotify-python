from yournotify import Yournotify

def test_import():
    assert Yournotify("x").api_url == "https://api.yournotify.com/"
