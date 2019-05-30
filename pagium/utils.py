# -*- coding: utf-8 -*-

import time
import socket
from functools import wraps
from typing import Union, Callable
from http.client import HTTPException

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


DEFAULT_POLLING_EXCEPTIONS = (
    IOError,
    OSError,
    HTTPException,
    WebDriverException,
)


DEFAULT_POLLING_TIMEOUT = 30
DEFAULT_POLLING_DELAY = 0.5


def polling(callback: Callable,
            timeout: Union[float, int] = DEFAULT_POLLING_TIMEOUT,
            delay: Union[float, int] = DEFAULT_POLLING_DELAY,
            except_exceptions=DEFAULT_POLLING_EXCEPTIONS):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            t_start = time.time()
            error = None

            while time.time() <= t_start + timeout:
                try:
                    return f(*args, **kwargs)
                except socket.error:
                    raise
                except except_exceptions as e:
                    error = e

                    if delay:
                        time.sleep(delay)

                    continue
            else:
                raise error

        return wrapped
    return wrapper(callback)


def waiting_for(callback: Callable,
                timeout: Union[float, int] = DEFAULT_POLLING_TIMEOUT,
                delay: Union[float, int] = DEFAULT_POLLING_DELAY,
                raise_exc=None,
                message: str = None,
                args: Union[list, tuple] = None,
                kwargs: dict = None):
    result = None

    args = args or tuple()
    kwargs = kwargs or dict()

    timeout = timeout or 0
    message = message or 'Timeout "{}" exceeded'.format(timeout)

    if timeout:
        t_start = time.time()

        while time.time() <= t_start + timeout:
            result = callback(*args, **kwargs)

            if result:
                return result

            if delay:
                time.sleep(delay)
        else:
            if raise_exc:
                raise raise_exc(message)

            return result

    result = callback(*args, **kwargs)

    if result:
        return result

    if raise_exc:
        raise raise_exc(message)

    return result


def get_driver(instance: Union[WebDriver, WebElement]):
    if isinstance(instance, WebDriver):
        return instance

    while not isinstance(instance, WebDriver):
        instance = instance.parent

    return instance
