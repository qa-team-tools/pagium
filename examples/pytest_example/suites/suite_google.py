# -*- coding: utf-8 -*-

import pytest
from pagium import Remote

from hamcrest import assert_that
from pagium.matchers import has_text, element_exists

from ..pages.google.search import GoogleSearchPage


@pytest.mark.parametrize('search_phrase', ['python selenium', 'page object'])
def test_search(browser: Remote, google_base_url: str, search_phrase: str):
    with GoogleSearchPage(browser, google_base_url) as page:
        page.search_form.input.fill(search_phrase)

    assert_that(page.result_container, element_exists(), has_text(search_phrase))
