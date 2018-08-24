from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select as SelectElement

from ..abilities.browse_the_web import BrowseTheWeb


class Strategy(Enum):
    value = "value"
    index = "index"
    text = "text"


def _select_by_value(element, option):
    return SelectElement(element).select_by_value(option)


def _select_by_index(element, option):
    return SelectElement(element).select_by_index(option)


def _select_by_text(element, option):
    return SelectElement(element).select_by_visible_text(option)


_selection_dict = {
    Strategy.value: _select_by_value,
    Strategy.index: _select_by_text,
    Strategy.text: _select_by_text
}


class Select:
    def __init__(self, option, locator=None, locator_strategy=By.CSS_SELECTOR, select_strategy=Strategy.text):
        self.locator = locator
        self.locator_strategy = locator_strategy
        self.option_to_select = option
        self.select_strategy = select_strategy

    @classmethod
    def option(cls, option):
        return cls(option)

    def by(self, strategy):
        self.select_strategy = strategy
        return self

    def from_dropdown(self, locator):
        try: # assume conforms to locator interface
            self.locator = locator.locator
            self.locator_strategy = locator.strategy
        except AttributeError:
            self.locator = locator
        return self

    def found(self, strategy):
        self.locator_strategy = strategy
        return self

    def perform_as(self, actor):
        element = actor.ability_to(BrowseTheWeb).driver.find_element(self.locator_strategy, self.locator)
        _selection_dict[self.select_strategy](element, self.option_to_select)