from typing import Union

import requests
from requests_html import HTMLSession, HTMLResponse, HTML

from scylla.loggings import logger


class Worker:

    def __init__(self):
        """Initialize the worker object

        """

        self.session = HTMLSession()

    def get_html(self, url: str, render_js: bool = True) -> Union[HTML, None]:
        """Get html from a specific URL

        :param url: the URL
        :param render_js: [whether to render js], defaults to True
        :param render_js: bool, optional
        :return: [the HTML string]
        :rtype: str
        """

        try:
            # TODO: load config for timeout
            response: HTMLResponse = self.session.get(url, timeout=30)
        except requests.RequestException:
            logger.warning('[Worker] Cannot get this url: ' + url)
            return None

        if response.ok:
            if render_js:
                print('starting render js...')
                response.html.render(wait=1.5, timeout=10.0)
                print('end render js...')
            return response.html
        else:
            return None
