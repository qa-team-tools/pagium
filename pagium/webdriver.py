# -*- coding: utf-8 -*-

from typing import Union
from contextlib import contextmanager

from selenium.webdriver import (
    Remote as _Remote,
    Chrome as _Chrome,
    Firefox as _Firefox,
    PhantomJS as _PhantomJS,
    Opera as _Opera,
    Safari as _Safari,
)

from pagium import utils


class WEbDriverPollingMixin:

    def __init__(self, *args, **kwargs):
        self._polling_timeout = kwargs.pop('polling_timeout', None)
        self._polling_delay = kwargs.pop('polling_delay', utils.DEFAULT_POLLING_DELAY)
        self._enable_polling = True if self._polling_timeout else False

        self._implicitly_wait = 0
        self._set_script_timeout = 0

        with self.disable_polling():
            super(WEbDriverPollingMixin, self).__init__(*args, **kwargs)

    @property
    def polling_timeout(self):
        return self._polling_timeout

    @property
    def polling_delay(self):
        return self._polling_delay

    @contextmanager
    def disable_polling(self, *, force=False):
        implicitly_wait = script_timeout = 0

        if force:
            implicitly_wait, script_timeout = self._implicitly_wait, self._set_script_timeout
            self.implicitly_wait(0)
            self.set_script_timeout(0)

        ep = self._enable_polling
        self._enable_polling = False

        try:
            yield
        finally:
            self._enable_polling = ep

            if force:
                self.implicitly_wait(implicitly_wait)
                self.set_script_timeout(script_timeout)

    @contextmanager
    def enable_polling(self,
                       timeout: Union[int, float] = utils.DEFAULT_POLLING_TIMEOUT,
                       delay: Union[int, float] = utils.DEFAULT_POLLING_DELAY):
        pt, pd, ep = self._polling_timeout, self._polling_delay, self._enable_polling
        self._polling_timeout, self._polling_delay, self._enable_polling = timeout, delay, True

        try:
            yield
        finally:
            self._polling_timeout, self._polling_delay, self._enable_polling = pt, pd, ep

    def execute(self, *args, **kwargs):
        if self._enable_polling:
            execute = utils.polling(
                super(WEbDriverPollingMixin, self).execute,
                timeout=self._polling_timeout, delay=self._polling_delay,
            )
        else:
            execute = super(WEbDriverPollingMixin, self).execute

        return execute(*args, **kwargs)

    def implicitly_wait(self, wait_timeout):
        self._implicitly_wait = wait_timeout
        super(WEbDriverPollingMixin, self).implicitly_wait(self._implicitly_wait)

    def set_script_timeout(self, wait_timeout):
        self._set_script_timeout = wait_timeout
        super(WEbDriverPollingMixin, self).set_script_timeout(self._set_script_timeout)


class Remote(WEbDriverPollingMixin, _Remote):
    """
    >>> wd = Remote(
    ... command_executor='http://localhost:4444/wd/hub',
    ... desired_capabilities={'browserName': 'chrome'},
    ... )

    >>> wd.quit()
    """
    pass


class Chrome(WEbDriverPollingMixin, _Chrome):
    pass


class Firefox(WEbDriverPollingMixin, _Firefox):
    pass


class PhantomJS(WEbDriverPollingMixin, _PhantomJS):
    pass


class Opera(WEbDriverPollingMixin, _Opera):
    pass


class Safari(WEbDriverPollingMixin, _Safari):
    pass
