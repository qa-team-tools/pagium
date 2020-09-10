# -*- coding: utf-8 -*-

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class Input(WebElement):

    @property
    def value(self):
        return self.get_attribute('value')

    @property
    def placeholder(self):
        return self.get_attribute('placeholder')

    def fill(self, text: str):
        self.clear()
        self.send_keys(*text)


class Link(WebElement):

    @property
    def href(self):
        return self.get_attribute('href')


class Image(WebElement):

    @property
    def src(self):
        return self.get_attribute('src')


class Select(WebElement):

    @property
    def options(self):
        return self.find_elements_by_tag_name('option')

    @property
    def selected(self):
        return next(iter([option for option in self.options if option.is_selected()]), None)

    def select(self, value, by='value'):
        for option in self.options:
            if (by == 'value' and option.get_attribute('value') == value) or (by == 'text' and option.text == value):
                option.click()
                break
        else:
            raise NoSuchElementException(f'Option "{value}" was not found')


class Checkbox(WebElement):

    def is_checked(self):
        return self.is_selected()

    def check(self):
        if not self.is_checked():
            self.click()

    def uncheck(self):
        if self.is_checked():
            self.click()
