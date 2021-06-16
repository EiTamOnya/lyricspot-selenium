"""Pages for the E2E tests."""
import os
import time


from locators import (
    SpotifyLoginPageLocators,
    SpotifyPlayerLocators,
    LoginPageLocators,
    MainPageLocators,)

username = os.getenv('USER')
password = os.getenv('PASS')


class Page(object):
    """Base object for all other pages."""

    def __init__(self, driver):
        self.driver = driver


class SpotifyLoginPage(Page):
    """Spotify login page methods."""
    def logging_in(self):
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
        self.driver.execute_script("window.open('https://lyric-spot.herokuapp.com/','_blank')")
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[1])

    def login_and_play_song(self, url):
        self.driver.get(url)
        self.click_login_button()
        self.logging_in()
        self.hide_warning_and_play()
        time.sleep(1.5)
        self.switch_to_new_tab()


class LoginPage(Page):
    """Login page methods."""
    def click_login_button(self):
        self.driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()


class MainPage(Page):
    """Main page methods."""
    def click_show_lyrics(self):
        self.driver.find_element(*MainPageLocators.LYRICS_BUTTON).click()

    def click_next_button(self):
        self.driver.find_element(*MainPageLocators.NEXT_BUTTON).click()

    def get_lyrics_button_text(self):
        return self.driver.find_element(*MainPageLocators.LYRICS_BUTTON).text

    def get_lyrics_context(self):
        return self.driver.find_element(*MainPageLocators.LYRICS_TEXT).text

    def get_song_name_text(self):
        return self.driver.find_element(*MainPageLocators.SONG_NAME).text