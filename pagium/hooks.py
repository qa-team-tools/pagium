# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys

from pagium.page import LazyWebElement


class BasePageElementHook:

    def __init__(self, web_element: LazyWebElement):
        self.web_element = web_element

    def __repr__(self):
        return f'Hook: {self.__class__.__name__}'


class ClickActionHook(BasePageElementHook):
    """
    >>> from pagium.webdriver import Remote
    >>> from pagium.page import PageElement, Page
    >>> from selenium.webdriver.common.by import By

    >>> wd = Remote(
    ... command_executor='http://localhost:4444/wd/hub',
    ... desired_capabilities={'browserName': 'chrome'},
    ... polling_timeout=10,
    ... polling_delay=0.5,
    ... )

    >>> class GooglePageTestBasic(Page):
    ...     search = PageElement(by=By.NAME, value='q')
    ...     submit = PageElement(by=By.NAME, value='btnK', hook=ClickActionHook)

    >>> with GooglePageTestBasic(wd, 'https://google.com') as page:
    ...     page.search.send_keys(*'python selenium')
    ...     page.submit()

    >>> wd.quit()
    """

    def __call__(self):
        self.web_element.click()


class SendEnterHook(BasePageElementHook):
    """
    >>> from pagium.webdriver import Remote
    >>> from pagium.page import PageElement, Page
    >>> from selenium.webdriver.common.by import By

    >>> wd = Remote(
    ... command_executor='http://localhost:4444/wd/hub',
    ... desired_capabilities={'browserName': 'chrome'},
    ... polling_timeout=10,
    ... polling_delay=0.5,
    ... )

    >>> class GooglePageTestBasic(Page):
    ...     search = PageElement(by=By.NAME, value='q', hook=SendEnterHook)

    >>> with GooglePageTestBasic(wd, 'https://google.com') as page:
    ...     page.search('python selenium')

    >>> wd.quit()
    """

    def __call__(self, text=None):
        if text is None:
            text = Keys.ENTER
        else:
            text = text + Keys.ENTER

        self.web_element.send_keys(*text)
