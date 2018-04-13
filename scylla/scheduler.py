from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process
from threading import Thread

from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip
from scylla.worker import Worker
from .loggings import logger
from .providers import BaseProvider, CoolProxyProvider, FreeProxyListProvider, KuaidailiProvider


def fetch_ips(q: Queue, validator_queue: Queue):
    logger.debug('fetch_ips...')
    worker = Worker()

    while True:
        provider: BaseProvider = q.get()

        provider_name = provider.__class__.__name__

        logger.debug('Get a provider from the provider queue: ' + provider_name)

        for url in provider.urls():
            html = worker.get_html(url)
            proxies = provider.parse(html)

            validator_queue.put(proxies)
            logger.info(
                ' {}: feed {} potential proxies into the validator queue'.format(provider_name, len(proxies))
            )


def validate_ips(q: Queue, validator_pool: ThreadPoolExecutor):
    proxies: [ProxyIP] = q.get()

    logger.debug('Validating {} ips...'.format(len(proxies)))

    for p in proxies:
        logger.debug('Submit ip: ' + p.__str__())
        validator_pool.submit(validate_proxy_ip, p=p)


class Scheduler(object):

    def __init__(self):
        self.worker_queue = Queue()
        self.validator_queue = Queue()
        self.worker_thread = None
        self.validator_thread = None
        self.validator_pool = ThreadPoolExecutor(max_workers=20)

    def start(self):
        logger.info('Scheduler starts...')
        self.feed_providers()

        self.worker_thread = Process(target=fetch_ips, args=(self.worker_queue, self.validator_queue))
        self.validator_thread = Thread(target=validate_ips, args=(self.validator_queue, self.validator_pool))

        self.worker_thread.start()
        self.validator_thread.start()

    def feed_providers(self):
        logger.debug('feed_providers...')
        self.worker_queue.put(CoolProxyProvider())
        self.worker_queue.put(FreeProxyListProvider())
        self.worker_queue.put(KuaidailiProvider())
