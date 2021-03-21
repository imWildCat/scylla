import requests
from playwright.sync_api import sync_playwright
from pyquery import PyQuery
from requests import Response
from typing import Union

from scylla.loggings import logger

DEFAULT_TIMEOUT_SECONDS = 30

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/89.0.4389.90 Safari/537.36 '


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

    # FIXME: Add back this test
    # sys:1: RuntimeWarning: coroutine 'Browser.new_page' was never awaited
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    # def _get_html_js(self, url: str) -> Union[PyQuery, None]:
    #     page = self.browser.new_page()
    #     response = page.goto(url=url, timeout=DEFAULT_TIMEOUT_SECONDS, wait_until='domcontentloaded')
    #
    #     if not response:
    #         logger.debug(f'Request for {url} failed because response is None')
    #         return None
    #
    #     if response.ok:
    #         doc = PyQuery(page.content())
    #         return doc
    #     else:
    #         logger.debug(f'Request for {url} failed, status code: {response.status}')
    #         return None
