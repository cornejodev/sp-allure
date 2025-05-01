def test_google_search_pass(browser):
    browser.get("https://www.google.com")
    assert "Google" in browser.title


def test_google_search_fail(browser):
    browser.get("https://www.google.com")
    assert "Googlee" in browser.title


# poetry env use python3
# eval $(poetry env activate)
# deactivate
