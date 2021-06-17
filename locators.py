"""Locators for the E2E tests."""
from selenium.webdriver.common.by import By


class SpotifyLoginPageLocators(object):
    """Class for the Spotify login page used in the tests."""
    USERNAME = (By.ID, 'login-username')
    PASSWORD = (By.ID, 'login-password')
    LOGIN_BUTTON = (By.ID, 'login-button')


class SpotifyPlayerLocators(object):
    """Class for the Spotify player page used in the tests."""
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-button"]')
    ACCEPT_COOCKIES = (By.ID, 'onetrust-accept-btn-handler')
    PLAY_BUTTON = (By.CSS_SELECTOR, '[data-testid="action-bar-row"] [data-testid="play-button"]')


class LoginPageLocators(object):
    """Class for the login page locators."""
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')


class MainPageLocators(object):
    """Class for the main page locators."""
    LYRICS_BUTTON = (By.ID, 'show-lyrics')
    LYRICS_TEXT = (By.ID, 'lyrics')
    TIMER = (By.CLASS_NAME, 'time')
    SONG_NAME = (By.CLASS_NAME, 'song-name')
    LOGOUT = (By.CSS_SELECTOR, '[href="/logout"]')
