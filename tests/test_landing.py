from po.landing_page import LandingPage


class TestLandingPage:

    def test_landing_page_google_pass(self, driver):
        landing_page = LandingPage(driver)
        landing_page.open_landing_page()
        assert landing_page.current_url == "https://www.google.com/"

    def test_landing_page_google_fail(self, driver):  # this will fail on purpose
        landing_page = LandingPage(driver)
        landing_page.open_landing_page()
        assert landing_page.current_url == "https://www.amazon.com/"


# poetry env use python3
# eval $(poetry env activate)
# deactivate
