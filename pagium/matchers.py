# -*- coding: utf8 -*-

from typing import Union
from urllib.parse import urlparse

from hamcrest.core.base_matcher import BaseMatcher
from selenium.webdriver.remote.webelement import WebElement

from pagium import utils
from pagium.page import Page, LazyWebElement


DEFAULT_TIMEOUT = 30
DEFAULT_DELAY = 0.5


class _BasePagiumMatcher(BaseMatcher):

    def __init__(self, *, timeout: int = DEFAULT_TIMEOUT, delay: float = DEFAULT_DELAY):
        self.timeout = timeout
        self.delay = delay


class _HasText(_BasePagiumMatcher):

    def __init__(self, text: str, **kwargs):
        super(_HasText, self).__init__(**kwargs)

        self.text = text

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


class _ElementExists(_BasePagiumMatcher):

    def __init__(self, count: int = 1, **kwargs):
        super(_ElementExists, self).__init__(**kwargs)

        self.count = count

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


class _URLPathEqual(_BasePagiumMatcher):

    def __init__(self, url_path: str, **kwargs):
        super(_URLPathEqual, self).__init__(**kwargs)

        self.url_path = url_path

    def _matches(self, browser):
        return utils.waiting_for(
            lambda: self.url_path == urlparse(browser.current_url).path,
            timeout=self.timeout,
            delay=self.delay,
            raise_exc=AssertionError,
        )

    def describe_to(self, description):
        description.append_text(
            f'Current path is not equal to "{self.url_path}"',
        )


url_path_equal = _URLPathEqual


class _URLPathContains(_BasePagiumMatcher):

    def __init__(self, url_path_part: str, **kwargs):
        super(_URLPathContains, self).__init__(**kwargs)

        self.url_path_part = url_path_part

    def _matches(self, browser):
        return utils.waiting_for(
            lambda: self.url_path_part in urlparse(browser.current_url).path,
            timeout=self.timeout,
            delay=self.delay,
            raise_exc=AssertionError,
        )

    def describe_to(self, description):
        description.append_text(
            f'Current path is not contains "{self.url_path_part}"',
        )


url_path_contains = _URLPathContains
