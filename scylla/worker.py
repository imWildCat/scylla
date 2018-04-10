from typing import Union

from requests_html import HTMLSession, HTMLResponse, HTML


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

        response: HTMLResponse = self.session.get(url)
        if response.ok:
            if render_js:
                response.html.render()
            return response.html
        else:
            return None
