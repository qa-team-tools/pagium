# -*- coding: utf8 -*-

from typing import Union

from hamcrest.core.base_matcher import BaseMatcher
from selenium.webdriver.remote.webelement import WebElement

from pagium import utils
from pagium.page import Page, LazyWebElement


DEFAULT_TIMEOUT = 30
DEFAULT_DELAY = 0.5


class _HasText(BaseMatcher):

    def __init__(self, text: str, timeout: int = DEFAULT_TIMEOUT, delay: float = DEFAULT_DELAY):
        self.text = text
        self.timeout = timeout
        self.delay = delay

    def _matches(self, instance: Union[Page, WebElement, LazyWebElement]):
        return utils.waiting_for(
            lambda: str(self.text).lower() in str(instance.text).lower(),
            timeout=self.timeout,
            delay=self.delay,
        )

    def describe_to(self, description):
        description.append_text(
            f'Text "{self.text}" exists on page (timeout: {self.timeout}, delay: {self.delay})',
        )


has_text = _HasText


class _ElementExists(BaseMatcher):

    def __init__(self, count: int = 1, timeout: int = DEFAULT_TIMEOUT, delay: float = DEFAULT_DELAY):
        self.count = count
        self.timeout = timeout
        self.delay = delay

    def _matches(self, lazy_web_element: LazyWebElement):
        driver = utils.get_driver(lazy_web_element.parent)

        def exists():
            if hasattr(driver, 'disable_polling'):
                with driver.disable_polling():
                    result = lazy_web_element.exists(self.count)
            else:
                result = lazy_web_element.exists(self.count)

            return result

        return utils.waiting_for(exists, timeout=self.timeout, delay=self.delay)

    def describe_to(self, description):
        description.append_text(
            f'Web element exists on page (timeout: {self.timeout}, delay: {self.delay}, count: {self.count})',
        )


element_exists = _ElementExists
