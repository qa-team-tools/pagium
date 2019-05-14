# -*- coding: utf8 -*-

import pytest
from _pytest.config import argparsing

from pagium import Remote


def pytest_addoption(parser: argparsing.Parser):
    """
    Add options here
    """
    parser.addoption(
        '--hub-tcp', action='store', default='localhost:4444', help='Selenium hub TCP',
    )
    parser.addoption(
        '--browser-name', action='store', default='chrome', help='Browser name',
    )
    parser.addoption(
        '--polling-timeout', action='store', type=int, default=30, help='Pagium polling timeout',
    )
    parser.addoption(
        '--polling-delay', action='store', type=float, default=0.5, help='Pagium polling delay',
    )


@pytest.fixture('session')
def hub_tcp(request):
    yield request.config.getoption('--hub-tcp')


@pytest.fixture('session')
def browser_name(request):
    yield request.config.getoption('--browser-name')


@pytest.fixture('session')
def google_base_url():
    yield 'http://google.com'


@pytest.fixture('function')
def browser(request, hub_tcp, browser_name):
    driver = Remote(
        command_executor=f'http://{hub_tcp}/wd/hub',
        desired_capabilities={'browserName': browser_name},
        polling_timeout=request.config.getoption('--polling-timeout'),
        polling_delay=request.config.getoption('--polling-delay'),
    )
    driver.maximize_window()

    try:
        yield driver
    finally:
        driver.quit()
