from typing import Union

import requests
from playwright.sync_api import sync_playwright
from pyquery import PyQuery
from requests import Response

from scylla.loggings import logger

DEFAULT_TIMEOUT_SECONDS = 200

DEFAULT_USER_AGENT = """Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A456 YaBrowser/19.5.2.38.10 YaApp_iOS/28.00 YaApp_iOS_Browser/28.00 Safari/602.1"""


class Worker:

    def __init__(self):
        """Initialize the worker object

        """

        with sync_playwright() as p:
            self.browser = p.chromium.launch()

        self.requests_session = requests.Session()
        self.requests_session.headers['User-Agent'] = DEFAULT_USER_AGENT

    def stop(self):
        """Clean the session
        """

        self.browser.close()

        self.requests_session.close()

    def get_html(self, url: str, render_js: bool = True) -> Union[PyQuery, None]:
        """Get html from a specific URL

        :param url: the URL
        :param render_js: [whether to render js], defaults to True
        :param render_js: bool, optional
        :return: [the HTML string]
        :rtype: str
        """

        if render_js:
            return self._get_html_js(url)
        else:
            return self._get_html_no_js(url)

    def _get_html_no_js(self, url: str) -> Union[PyQuery, None]:
        try:
            # TODO: load config for timeout
            response: Response = self.requests_session.get(url, timeout=DEFAULT_TIMEOUT_SECONDS)
        except requests.RequestException:
            logger.warning('[Worker] Cannot get this url: ' + url)
            return None
        except (KeyboardInterrupt, SystemExit, InterruptedError):
            self.stop()
            return None

        if response.ok:
            doc = PyQuery(response.text)
            return doc
        else:
            logger.debug(f'Request for {url} failed, status code: {response.status_code}')
            return None

    def _get_html_js(self, url: str) -> Union[PyQuery, None]:
        page = self.browser.new_page()
        response = page.goto(url=url, timeout=DEFAULT_TIMEOUT_SECONDS, wait_until='domcontentloaded')

        if not response:
            logger.debug(f'Request for {url} failed because response is None')
            return None

        if response.ok:
            doc = PyQuery(page.content())
            return doc
        else:
            logger.debug(f'Request for {url} failed, status code: {response.status}')
            return None
