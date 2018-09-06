# -*- coding: utf-8 -*-

from pagium import Page, PageElement, WebElement, By, Keys


class SearchInput(WebElement):

    def fill(self, text):
        self.send_keys(*text + Keys.ENTER)


class SearchForm(WebElement):

    input = PageElement(SearchInput, by=By.NAME, value='q')


class GoogleSearchPage(Page):

    search_form = PageElement(SearchForm)
    result_container = PageElement(by=By.ID, value='center_col')
