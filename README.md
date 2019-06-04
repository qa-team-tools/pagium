About this
==========

This is page object implementation for selenium library.

Installation
============

```bash
pip install pagium
```

How to use
==========

Basic usage
-----------

```python
from pagium import Page, PageElement, By, Remote


class GooglePage(Page):

    search = PageElement(by=By.NAME, value='q')


wd = Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities={'browserName': 'chrome'},
)

with GooglePage(wd, 'https://google.com') as page:
    page.search.send_keys(*'python selenium')
```

Controls usage
--------------

```python
from pagium import Page, PageElement, By, controls


class GooglePage(Page):

    search = PageElement(controls.Input, by=By.NAME, value='q')
```

Container usage
---------------

```python
from pagium import Page, PageElement, WebElement, By, controls


class SearchForm(WebElement):

    input = PageElement(controls.Input, by=By.NAME, value='q')


class GooglePage(Page):

    search_form = PageElement(SearchForm)
```

Page element hook
-----------------

```python
from pagium import PageElement, WebElement, By, Keys, controls


class SearchForm(WebElement):

    input = PageElement(controls.Input, by=By.NAME, value='q')

    submit = PageElement(by=By.NAME, value='q', hook=lambda we: we.send_keys(Keys.ENTER))
```

Web driver polling
------------------

Pagium has feature polling for web drivers

```python
from pagium import Remote


wd = Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities={'browserName': 'chrome'},
    polling_timeout=20,
    polling_delay=0.5,
)
```

Polling timeout is retry time for a while command execution raising error and delay is sleep time between retries.

It can be using like

```python
from pagium import Remote


wd = Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities={'browserName': 'chrome'},
)

with wd.enable_polling(20, delay=0.1):
    ...
```

or like

```python
from pagium import Remote


wd = Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities={'browserName': 'chrome'},
    polling_timeout=20,
    polling_delay=0.5,
)

with wd.disable_polling():
    ...
```

Assert matchers
---------------

```python
from hamcrest import assert_that
from pagium.matchers import element_exists, has_text, match_regexp, url_path_equal, url_path_contains


assert_that(page, url_path_contains('/se'))
assert_that(page, url_path_equal('/search'))
assert_that(page.result_container, element_exists())
assert_that(page.result_container, match_regexp('[a-z]+'))
assert_that(page.result_container, has_text('page object'))
```
