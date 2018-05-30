import random
import sys
import traceback
from multiprocessing import Process

from tornado import httpclient, web, ioloop
from tornado.httpclient import HTTPResponse

from scylla.config import get_config
from scylla.database import ProxyIP
from scylla.loggings import logger

# Using CurlAsyncHTTPClient because its proxy support
httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")


def get_proxy(https=False) -> ProxyIP:
    proxies: [ProxyIP] = ProxyIP.select().where(ProxyIP.is_valid == True).where(ProxyIP.stability >= 0.9)

    if https:
        proxies = proxies.where(ProxyIP.is_https == True)

    proxies = proxies.order_by(ProxyIP.updated_at.desc()).limit(63)
    proxy: ProxyIP = random.choice(proxies)

    return proxy


# TODO: handle https requests
class ForwardingRequestHandler(web.RequestHandler):
    """
    A very rough ForwardingRequestHandler, only supports HTTP requests.
    """

    def data_received(self, chunk):
        pass

    def get_proxy_and_forward(self):
        https = False

        # At present, this proxy does not support https
        if self.request.uri.startswith('https'):
            https = True

        disable_forward_proxy = get_config('disable_forward_proxy', default=False)

        if disable_forward_proxy:
            self.forward()
        else:
            proxy = get_proxy(https=https)
            self.forward(host=proxy.ip, port=proxy.port)

    @web.asynchronous
    def get(self, *args, **kwargs):
        self.get_proxy_and_forward()

    @web.asynchronous
    def post(self, *args, **kwargs):
        self.get_proxy_and_forward()

    def handle_response(self, response: HTTPResponse):

        if response.body:
            self.write(response.body)
            self.finish()
        elif response.error:
            logger.debug('The forward proxy has an error: {}'.format(response.error))
            self.finish()
        else:
            self.finish()

    def forward(self, host=None, port=None):
        try:
            url = self.request.uri

            body = self.request.body

            if not body:
                body = None

            httpclient.AsyncHTTPClient().fetch(
                httpclient.HTTPRequest(
                    url=url,
                    method=self.request.method,
                    body=body,
                    headers=self.request.headers,
                    follow_redirects=False,
                    validate_cert=False,
                    proxy_host=host,
                    proxy_port=port),
                self.handle_response)

        except httpclient.HTTPError as e:
            logger.debug("tornado signalled HTTPError {}".format(e))
            self.set_status(500)
            self.finish()
        except:
            self.set_status(500)
            self.write("Internal server error:\n" +
                       ''.join(traceback.format_exception(*sys.exc_info())))
            self.finish()


def make_app():
    return web.Application([
        (r'.*', ForwardingRequestHandler),
    ])


def start_forward_proxy_server():
    app = make_app()
    port = int(get_config('proxy_port', default='8081'))
    app.listen(port)
    logger.info('Start forward proxy server on port {}'.format(port))
    ioloop.IOLoop.current().start()


def start_forward_proxy_server_non_blocking():
    p = Process(target=start_forward_proxy_server, daemon=True)
    p.start()
