"""Pages for the E2E tests."""
import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import (
    SpotifyLoginPageLocators,
    SpotifyPlayerLocators,
    LoginPageLocators,
    MainPageLocators,
)


HOME_URL = "https://lyric-spot-staging.herokuapp.com/"
username = os.getenv("USER")
password = os.getenv("PASS")


class Page(object):
    """Base object for all other pages."""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element_text(self, element, text):
        WebDriverWait(self.driver, 10).until_not(
            EC.text_to_be_present_in_element(element, text)
        )

    def driver_wait(self, seconds):
        WebDriverWait(self.driver, seconds)


class SpotifyLoginPage(Page):
    """Spotify login page methods."""

    def spotify_log_in(self):
        self.driver.find_element(*SpotifyLoginPageLocators.USERNAME).send_keys(username)
        self.driver.find_element(*SpotifyLoginPageLocators.PASSWORD).send_keys(password)
        self.driver.find_element(*SpotifyLoginPageLocators.LOGIN_BUTTON).click()


class SpotifyPlayerPage(SpotifyLoginPage):
    """Spotify player page methods."""

    def click_login_button(self):
        self.driver.find_element(*SpotifyPlayerLocators.LOGIN_BUTTON).click()

    def hide_warning_and_play(self):
        self.driver.find_element(*SpotifyPlayerLocators.ACCEPT_COOCKIES).click()
        time.sleep(1.5)
        self.driver.find_element(*SpotifyPlayerLocators.PLAY_BUTTON).click()

    def switch_to_new_tab(self):
        self.driver.execute_script(
            "window.open('https://lyric-spot-staging.herokuapp.com/','_blank')"
        )
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])

    def login_and_play_song(self, url):
        self.driver.get(url)
        self.click_login_button()
        self.spotify_log_in()
        self.hide_warning_and_play()
        time.sleep(1.5)
        self.switch_to_new_tab()


class LoginPage(SpotifyLoginPage):
    """Login page methods."""

    def get_login_button(self):
        return self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON)

    def click_login_button(self):
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

    def log_in(self):
        self.driver.get(HOME_URL)
        self.click_login_button()
        self.spotify_log_in()


class MainPage(Page):
    """Main page methods."""

    def click_show_lyrics(self):
        self.driver.find_element(*MainPageLocators.LYRICS_BUTTON).click()

    def click_next_button(self):
        self.driver.find_element(*MainPageLocators.NEXT_BUTTON).click()

    def get_lyrics_button(self):
        return self.driver.find_element(*MainPageLocators.LYRICS_BUTTON)

    def get_lyrics_content(self):
        return self.driver.find_element(*MainPageLocators.LYRICS_TEXT)

    def get_song_name(self):
        return self.driver.find_element(*MainPageLocators.SONG_NAME)

    def get_logout_link(self):
        return self.driver.find_element(*MainPageLocators.LOGOUT)

    def wait_for_lyrics(self):
        self.wait_for_element_text(MainPageLocators.LYRICS_TEXT, "Fetching lyrics...")

    def get_top_tracks(self):
        return self.driver.find_element(*MainPageLocators.TOP)

    def get_recent_tracks(self):
        return self.driver.find_element(*MainPageLocators.RECENT)

    def get_page_title(self):
        return self.driver.find_element(*MainPageLocators.TITLE)

    def get_all_song_names(self):
        return self.driver.find_elements(*MainPageLocators.SONG_NAME)

    def get_all_song_artists(self):
        return self.driver.find_elements(*MainPageLocators.ARTIST_NAME)

    def get_mode_link(self):
        return self.driver.find_element(*MainPageLocators.MODE)
