import playwright
from playwright.sync_api import Browser
from requests_html import HTML
from typing import Union
from pyquery import PyQuery

import requests
from playwright import sync_playwright, SyncPlaywrightContextManager

from scylla.loggings import logger


class Worker:
    browser: Browser

    def __init__(self):
        """Initialize the worker object

        """

        with sync_playwright() as p:
            self.browser = p.chromium.launch()

    def stop(self):
        """Clean the session
        """

        self.browser.close()

    def get_html(self, url: str, render_js: bool = True) -> Union[PyQuery, None]:
        """Get html from a specific URL

        :param url: the URL
        :return: [the HTML string]
        :rtype: str
        """

        try:
            # TODO: load config for timeout
            page = self.browser.newPage()
            page.goto(url=url, timeout=30, waitUntil='networkidle', referer=url)
            html_content = page.content()
            doc = PyQuery(html_content)
            return doc
        except playwright.TimeoutError:
            logger.warning('[Worker] Cannot get this url (timeout): ' + url)
            return None
        except (KeyboardInterrupt, SystemExit, InterruptedError):
            self.stop()
            return None
