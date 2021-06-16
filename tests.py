"""E2E test cases for the lyricspot app."""
import requests
import unittest

from page import (
    LoginPage,
    SpotifyLoginPage,
    SpotifyPlayerPage,
    MainPage)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOME_URL = 'https://lyric-spot.herokuapp.com/'


class LyricspotTestCase(unittest.TestCase):
    """E2E test cases for the lyricspot app."""

    @classmethod
    def setUpClass(cls):
        # Make sure that the dyno is awake before continuing with the tests
        resp = requests.get(HOME_URL)
        assert(resp.status_code == 200)

    def setUp(self):
        self.driver = webdriver.Chrome(r'driver\\chromedriver.exe')
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.login_page = LoginPage(self.driver)
        self.spotify_login = SpotifyLoginPage(self.driver)
        self.spotify_player = SpotifyPlayerPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.addCleanup(self.driver.quit)

    def test_page_title(self):
        """Test the title of the webpage."""
        self.driver.get(HOME_URL)
        self.assertIn('Lyricspot', self.driver.title)

    def test_logging_in(self):
        """Test the logging in functionality."""
        self.driver.get(HOME_URL)
        self.login_page.click_login_button()
        self.spotify_login.logging_in()
        self.assertEquals('Show Lyrics', self.main_page.get_lyrics_button_text())

    def test_check_lyrics(self):
        """Test for checking if the correct song lyrics are shown."""
        self.spotify_player.login_and_play_song('https://open.spotify.com/album/2XPrwlaAHHXnJzP9tBcIzH')

        self.login_page.click_login_button()
        self.main_page.click_show_lyrics()

        # wait for the lyrics to load
        WebDriverWait(self.driver, 10).until_not(
                EC.text_to_be_present_in_element((By.ID, "lyrics"), "Fetching lyrics...")
            )

        expected_name = 'Swimming Pools (Drank)'
        expected_text = 'Pool full of liquor, then you dive in it'

        self.assertEqual(expected_name, self.main_page.get_song_name_text())
        self.assertTrue(expected_text in self.main_page.get_lyrics_context())


if __name__ == '__main__':
    unittest.main(verbosity=2)
