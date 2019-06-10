# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from pagium.page import LazyWebElement


class BasePageElementHook:

    def __init__(self, web_element: LazyWebElement):
        self.web_element = web_element

    def __repr__(self):
        return f'Hook: {self.__class__.__name__}'


class ClickActionHook(BasePageElementHook):

    def __call__(self):
        self.web_element.click()


class SendEnterHook(BasePageElementHook):

    def __call__(self, text=None):
        if text in None:
            text = Keys.ENTER
        else:
            text = text + Keys.ENTER

        self.web_element.send_keys(*text)
