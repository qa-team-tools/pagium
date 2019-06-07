

"""
>>> from pagium.webdriver import Remote
>>> from selenium.webdriver.common.by import By
>>> from selenium.webdriver.common.keys import Keys

>>> wd = Remote(
... command_executor='http://localhost:4444/wd/hub',
... desired_capabilities={'browserName': 'chrome'},
... polling_timeout=10,
... polling_delay=0.5,
... )

>>> class GooglePageTestBasic(Page):
...     search = PageElement(by=By.NAME, value='q')

>>> with GooglePageTestBasic(wd, 'https://google.com') as page:
...     page.search.send_keys(*'python selenium' + Keys.ENTER)

>>> with GooglePageTestBasic(wd, 'https://google.com') as page:
...     assert page.search.exists() == True

>>> class SearchInput(WebElement):
...     def fill(self, text):
...         self.send_keys(*text + Keys.ENTER)

>>> class GooglePageTestControl(Page):
...     search = PageElement(SearchInput, by=By.NAME, value='q')

>>> with GooglePageTestControl(wd, 'https://google.com') as page:
...     page.search.fill('python selenium')

>>> class SearchForm(WebElement):
...     input = PageElement(SearchInput, by=By.NAME, value='q')

>>> class GooglePageTestSeparatedComponent(Page):
...     search_form = PageElement(SearchForm)

>>> with GooglePageTestSeparatedComponent(wd, 'https://google.com') as page:
...     page.search_form.input.fill('python selenium')

>>> wd.quit()
"""

from typing import Union, Callable
from urllib.parse import urljoin

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Page:

    __path__ = None

    def __init__(self, parent: Union[WebDriver, WebElement], url: str, **options):
        """
        >>> assert Page(object, 'http://google.com').url ==  'http://google.com'

        >>> class TestPage(Page):
        ...     __path__ = '/test/{param}'

        >>> assert TestPage(
        ... object, 'http://google.com', path={'param': 'one'},
        ... ).url == 'http://google.com/test/one'

        >>> assert TestPage(object, '').parent == object

        >>> assert 'test' in TestPage(object, '', test=1).options
        """
        self._url = url

        self._parent = parent
        self._options = options

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def __getattr__(self, item):
        return getattr(self._parent, item)

    def __repr__(self):
        return f'<{self.__class__.__name__} on {self.url}>'

    @property
    def parent(self):
        return self._parent

    @property
    def options(self):
        return self._options

    @property
    def text(self) -> str:
        if isinstance(self._parent, WebDriver):
            return str(self._parent.find_element_by_tag_name('body').text)
        return str(self._parent.text)

    @property
    def url(self):
        if self.__path__ is not None:
            return urljoin(
                self._url, self.__path__.format(
                    **self._options.get('path', {}),
                ),
            )

        return self._url

    def open(self):
        if isinstance(self._parent, WebDriver):
            self._parent.get(self.url)
        else:
            raise AssertionError(
                'Can not open page because parent is not instance of WebDriver object',
            )

    def close(self):
        pass


class PageElement:

    def __init__(self,
                 we_class: type = None,
                 by: str = None,
                 value: str = None,
                 is_list: bool = False,
                 hook: Callable = None):
        if we_class is not None:
            if not issubclass(we_class, WebElement):
                raise AssertionError(
                    'Web element type can be subclass of WebElement only',
                )

        if by is None and value is None and we_class is None:
            raise AssertionError(
                '"by", "value" or "we_type" is required params for search web element',
            )

        self._we_class = we_class
        self._by = by
        self._value = value
        self._is_list = is_list
        self._hook = hook

    def __repr__(self):
        we_class = self._we_class or WebElement
        return f'{we_class.__name__}: {self._by}={self._value} '

    def __get__(self, instance: Union[Page, WebElement], owner: type):
        parent = instance

        if isinstance(instance, Page):
            parent = instance.parent

        lazy_web_element = LazyWebElement(self, parent)

        if callable(self._hook):
            return self._hook(lazy_web_element)

        return lazy_web_element

    @property
    def by(self):
        return self._by

    @property
    def we_class(self):
        return self._we_class

    @property
    def value(self):
        return self._value

    @property
    def is_list(self):
        return self._is_list

    def get(self, parent: Union[WebDriver, WebElement]) -> Union[WebElement, list]:
        if self._by is None and self._value is None:
            if self._we_class is None:
                raise AssertionError(
                    'Can not create web element container, use "we_type" param for resolve it',
                )
            container = self._we_class(parent, parent.session_id)
            container.find_element = parent.find_element
            container.find_elements = parent.find_elements

            return container

        if self._is_list:
            web_element = parent.find_elements(by=self._by, value=self._value)

            if self._we_class is not None:
                for we in web_element:
                    we.__class__ = self._we_class
        else:
            web_element = parent.find_element(by=self._by, value=self._value)

            if self._we_class is not None:
                web_element.__class__ = self._we_class

        return web_element


class LazyWebElement:

    def __init__(self, element: PageElement, parent: Union[WebDriver, WebElement]):
        self._page_element = element
        self._parent = parent
        self._web_element = None

    def __repr__(self):
        self._search()
        return f'{self.__class__.__name__} -> {repr(self._web_element)}'

    def __iter__(self):
        self._search()
        return iter(self._web_element)

    def __getattr__(self, item):
        self._search()
        return getattr(self._web_element, item)

    def __getitem__(self, item):
        self._search()
        return self._web_element.__getitem__(item)

    def __len__(self):
        self._search()
        if self._page_element.is_list:
            return self._web_element.__len__()

        return 1

    def _search(self):
        if self._web_element is None:
            self._web_element = self._page_element.get(self._parent)

    @property
    def parent(self):
        return self._parent

    def exists(self, count: int = 1) -> bool:
        self.refresh()

        try:
            self._search()
        except WebDriverException:
            return False

        if self._page_element.is_list:
            return len(self._web_element) >= count

        return self._web_element.is_displayed()

    def refresh(self):
        self._web_element = None
