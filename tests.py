"""E2E test cases for the lyricspot app."""
import requests
import unittest

from sys import platform

from page import LoginPage, SpotifyLoginPage, SpotifyPlayerPage, MainPage, HOME_URL

from selenium import webdriver


class LyricspotTestCase(unittest.TestCase):
    """E2E test cases for the lyricspot app."""

    @classmethod
    def setUpClass(cls):
        # Make sure that the dyno is awake before continuing with the tests
        resp = requests.get(HOME_URL)
        assert resp.status_code == 200

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        if platform == "linux" or platform == "linux2":
            # options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(r"driver/chromedriver", options=options)
        elif platform == "win32":
            self.driver = webdriver.Chrome(r"driver\\chromedriver.exe", options=options)
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
        self.assertIn("Lyricspot", self.driver.title)

    def test_logging_in_and_out(self):
        """Test the logging in functionality."""
        self.login_page.log_in()
        self.assertEquals("Log out", self.main_page.get_logout_link().text)
        self.main_page.get_logout_link().click()
        self.assertEquals("Login with Spotify", self.login_page.get_login_button().text)

    def test_lyrics_button(self):
        self.login_page.log_in()
        self.assertEquals("Show Lyrics", self.main_page.get_lyrics_button().text)
        self.main_page.click_show_lyrics()
        self.assertEquals("Hide Lyrics", self.main_page.get_lyrics_button().text)

    @unittest.skipIf(
        platform != "win32",
        "This doesn't work in headless and is covered by the e2e tests.",
    )
    def test_check_lyrics(self):
        """Test for checking if the correct song lyrics are shown."""

        # SHOULD ADD AN ENDPOINT THAT DOES THAT FOR ME
        self.spotify_player.login_and_play_song(
            "https://open.spotify.com/album/2kKXGWaCEl06EKZ4DxBJIT"
        )

        self.login_page.click_login_button()
        self.main_page.click_show_lyrics()
        self.main_page.wait_for_lyrics()

        expected_name = "Dream House"
        expected_text = "I want to dream"

        self.assertEqual(expected_name, self.main_page.get_song_name().text)
        self.assertTrue(expected_text in self.main_page.get_lyrics_content().text)

    def test_check_top_tracks(self):
        """Test for checking if the top tracks are shown."""
        self.login_page.log_in()
        self.main_page.get_top_tracks().click()
        self.assertTrue(
            "Your 50 Top Played Tracks" in self.main_page.get_page_title().text
        )
        artists = [artist.text for artist in self.main_page.get_all_song_artists()]
        self.assertTrue("Deafheaven" in artists)

    def test_check_recent_tracks(self):
        """Test for checking if the top tracks are shown."""
        self.login_page.log_in()
        self.main_page.get_recent_tracks().click()
        self.assertTrue(
            "Your 50 Recently Played Tracks" in self.main_page.get_page_title().text
        )
        song_names = [song.text for song in self.main_page.get_all_song_names()]
        self.assertTrue("Dream House" in song_names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
