# -*- coding: utf-8 -*-

import nose
import json
from unittest import TestCase

from pagium import Remote
from allure.constants import AttachmentType

from . import config


class PagiumTestSuite(TestCase):

    def setUp(self):
        self.browser = Remote(
            command_executor=f'http://{config.HUB_TCP}/wd/hub',
            desired_capabilities={'browserName': config.BROWSER_NAME},
            polling_timeout=config.POLLING_TIMEOUT,
            polling_delay=config.POLLING_DELAY,
        )

    def tearDown(self):
        try:
            nose.allure.attach(
                'Screenshoot', self.browser.get_screenshot_as_png(), AttachmentType.PNG,
            )

            for log_type in self.browser.log_types:
                content = json.dumps(self.browser.get_log(log_type), indent=2)
                nose.allure.attach(
                    'Got {} log'.format(log_type), content, AttachmentType.JSON,
                )
        finally:
            self.browser.quit()

