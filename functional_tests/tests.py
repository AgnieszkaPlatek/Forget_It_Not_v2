from selenium import webdriver
from django.test import LiveServerTestCase

# class NewVisitorTest(unittest.TestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Chrome('../chromedriver.exe')
#
#     def tearDown(self) -> None:
#         self.browser.quit()
#
#     def test_enter_api_root(self):
#         self.browser.get('http://localhost:8000/api/')
#
#         self.assertIn('Api Root', self.browser.title)


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('./chromedriver.exe')

    def tearDown(self) -> None:
        self.browser.quit()

    def test_enter_api_root(self):
        self.browser.get(self.live_server_url + '/api/')

        self.assertIn('Api Root', self.browser.title)
