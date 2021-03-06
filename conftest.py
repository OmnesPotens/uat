"""Test fixtures for selenium UAT for adventurer's codex."""

import pytest

from selenium import webdriver

from components.core.general.new_character_campaign import NewCharacterCampaign
from components.core.character import wizard
from components.core.dm.wizard import TellUsAStory
from utils import utils as ut


def pytest_addoption(parser):
    """Command line parameters."""
    parser.addoption('--web_driver', action='store', default='chrome')
    parser.addoption(
        '--url',
        action='store',
        default='https://nightly.adventurerscodex.com'
    )


@pytest.fixture
def web_driver(request):
    """Return command line argument."""
    return request.config.getoption('--web_driver')


@pytest.fixture
def url(request):
    """Return command line argument."""
    return request.config.getoption('--url')


@pytest.fixture(scope='function')
def browser(request, web_driver, url):
    """Return selenium webdriver chrome instance."""
    driver = None
    if web_driver.lower() == 'chrome':
        driver = webdriver.Chrome()

    elif web_driver.lower() == 'firefox':
        driver = webdriver.Firefox()

    elif web_driver.lower() == 'safari':
        driver = webdriver.Safari()

    driver.get(url)
    driver.implicitly_wait(10)

    def close_browser():
        driver.quit()

    request.addfinalizer(close_browser)

    return driver


@pytest.fixture(scope='function')
def dm_wizard(browser):
    """Navigate through the dm wizard."""
    wizard_main = NewCharacterCampaign(browser)
    tell_us_a_story = TellUsAStory(browser)

    wizard_main.get_started.click()
    wizard_main.dm.click()
    wizard_main.next_.click()

    tell_us_a_story.campaign_name = 'Test Campaign'
    tell_us_a_story.player_name = 'Automated Testing Bot.'

    wizard_main.finish.click()


@pytest.fixture(scope='function')
def player_wizard(browser):
    """Navigate through the player wizard."""
    wizard_main = NewCharacterCampaign(browser)
    who_are_you = wizard.WhoAreYou(browser)
    ability_scores = wizard.AbilityScoresManual(browser)

    wizard_main.get_started.click()
    wizard_main.player.click()
    wizard_main.next_.click()

    who_are_you.character_name = 'Test Char'
    who_are_you.player_name = 'Automated Testing Bot.'

    wizard_main.next_.click()

    ability_scores.strength = '18'
    ability_scores.dexterity = '18'
    ability_scores.constitution = '18'
    ability_scores.intelligence = '18'
    ability_scores.wisdom = '18'
    ability_scores.charisma = '18'

    wizard_main.finish.click()
