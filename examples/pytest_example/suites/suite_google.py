# -*- coding: utf-8 -*-

import pytest
from pagium import Remote

from hamcrest import assert_that
from pagium.matchers import has_text, element_exists, url_path_equal

from ..pages.google.search import GoogleSearchPage


@pytest.mark.parametrize('search_phrase', ['python selenium', 'page object'])
def test_search(browser: Remote, google_base_url: str, search_phrase: str):
    with GoogleSearchPage(browser, google_base_url) as page:
        page.search_form.input.fill(search_phrase)

    assert_that(page.result_container, element_exists())
    assert_that(page.result_container, has_text(search_phrase))

    assert_that(browser, url_path_equal('/search'))
