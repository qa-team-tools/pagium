# -*- coding: utf-8 -*-

from hamcrest import assert_that
from nose_parameterized import parameterized
from pagium.matchers import has_text, element_exists

from ..case import PagiumTestSuite
from ..pages.google.search import GoogleSearchPage


class GoogleTestSuite(PagiumTestSuite):

    @parameterized.expand([
        ('page object', ),
        ('python selenium', ),
    ])
    def test_search(self, search_phrase):
        with GoogleSearchPage(self.browser, 'http://google.com') as page:
            page.search_form.input.fill(search_phrase)

        assert_that(page.result_container, element_exists(), has_text(search_phrase))
