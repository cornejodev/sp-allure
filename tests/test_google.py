def test_google_search(browser):
    browser.get("https://www.google.com")
    assert "Googlee" in browser.title


# poetry env use python3
# eval $(poetry env activate)
# deactivate
