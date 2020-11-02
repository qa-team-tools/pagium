# -*- coding: utf8 -*-

import re
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

    def __matches__(self, *args, **kwargs):
        pass

    def _matches(self, *args, **kwargs):
        return utils.waiting_for(
            self.__matches__, args=args, kwargs=kwargs,
            timeout=self.timeout, delay=self.delay,
        )

    def _create_message(self, text, **params):
        params.update(timeout=self.timeout, delay=self.delay)
        params_string = ', '.join(f'{k}={v}' for k, v in params.items())

        return f'{text} ({params_string})'


class _HasText(_BasePagiumMatcher):

    def __init__(self, text: str, **kwargs):
        super(_HasText, self).__init__(**kwargs)
        self.text = text

    def __matches__(self, instance: Union[Page, WebElement, LazyWebElement]):
        if isinstance(instance, LazyWebElement):
            instance.refresh()
        self.actual_text = instance.text
        return str(self.text).lower() in str(self.actual_text).lower()

    def describe_to(self, description):
        description.append_text(
            self._create_message(f'Text "{self.text}" exists'),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'was {self.actual_text}')


has_text = _HasText


class _ElementExists(_BasePagiumMatcher):

    def __init__(self, count: int = 1, **kwargs):
        super(_ElementExists, self).__init__(**kwargs)

        self.count = count

    def __matches__(self, lazy_web_element: LazyWebElement):
        driver = utils.get_driver(lazy_web_element.parent)

        if hasattr(driver, 'disable_polling'):
            with driver.disable_polling(force=True):
                result = lazy_web_element.exists(self.count)
        else:
            result = lazy_web_element.exists(self.count)

        return result

    def describe_to(self, description):
        description.append_text(
            self._create_message('Web element exists', count=self.count),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was not found')


element_exists = _ElementExists


class _ElementNotExists(_BasePagiumMatcher):

    def __init__(self, count: int = 1, **kwargs):
        super(_ElementNotExists, self).__init__(**kwargs)

        self.count = count

    def __matches__(self, lazy_web_element: LazyWebElement):
        driver = utils.get_driver(lazy_web_element.parent)

        if hasattr(driver, 'disable_polling'):
            with driver.disable_polling(force=True):
                result = not lazy_web_element.exists(self.count)
        else:
            result = not lazy_web_element.exists(self.count)

        return result

    def describe_to(self, description):
        description.append_text(
            self._create_message('Web element not exists', count=self.count),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was found')


element_not_exists = _ElementNotExists


class _URLPathEqual(_BasePagiumMatcher):

    def __init__(self, url_path: str, **kwargs):
        super(_URLPathEqual, self).__init__(**kwargs)

        self.url_path = url_path
        self.current_path = None

    def __matches__(self, browser):
        self.current_path = urlparse(browser.current_url).path
        return self.url_path == self.current_path

    def describe_to(self, description):
        description.append_text(
            self._create_message(f'Current path equal to "{self.url_path}"'),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'was "{self.current_path}"')


url_path_equal = _URLPathEqual


class _URLPathContains(_BasePagiumMatcher):

    def __init__(self, url_path_part: str, **kwargs):
        super(_URLPathContains, self).__init__(**kwargs)

        self.url_path_part = url_path_part
        self.current_path = None

    def __matches__(self, browser):
        self.current_path = urlparse(browser.current_url).path
        return self.url_path_part in self.current_path

    def describe_to(self, description):
        description.append_text(
            self._create_message(f'Current path contains "{self.url_path_part}"'),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'was "{self.current_path}"')


url_path_contains = _URLPathContains


class _MatchRegexp(_BasePagiumMatcher):

    def __init__(self, regexp, **kwargs):
        super(_MatchRegexp, self).__init__(**kwargs)

        self.pattern = re.compile(regexp)

    def __matches__(self, instance):
        if instance(instance, LazyWebElement):
            instance.refresh()
        self.text = instance.text
        return self.pattern.search(self.text) is not None

    def describe_to(self, description):
        description.append_text(
            self._create_message(f'a element text matching "{self.pattern.pattern}"'),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'was "{self.text}"')


match_regexp = _MatchRegexp


class _TagAttributeEqual(_BasePagiumMatcher):

    def __init__(self, attribute_name, value, **kwargs):
        super(_TagAttributeEqual, self).__init__(**kwargs)
        self.attribute_name = attribute_name
        self.value = value

    def __matches__(self, we: Union[WebElement, LazyWebElement]):
        return we.get_attribute(self.attribute_name) == self.value

    def describe_to(self, description):
        description.append_text(
            self._create_message(f'Attribute value:"{self.value}" equals'),
        )

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text('was not equals')


tag_attribute_equal = _TagAttributeEqual
