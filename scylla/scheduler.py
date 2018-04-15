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

            for p in proxies:
                validator_queue.put(p)

            logger.info(
                ' {}: feed {} potential proxies into the validator queue'.format(provider_name, len(proxies))
            )


def validate_ips(q: Queue, validator_pool: ThreadPoolExecutor):
    proxy: ProxyIP = q.get()

    validator_pool.submit(validate_proxy_ip, p=proxy)

    # Not supported on macOS:
    # q_size = q.qsize()
    # if q_size == 0:
    #     logger.debug('There is no ip left to be validated temporarily.')
    # else:
    #     logger.debug('There are/is {} ip(s) left to be validated.'.format(q_size))


class Scheduler(object):

    def __init__(self):
        self.worker_queue = Queue()
        self.validator_queue = Queue()
        self.worker_process = None
        self.validator_thread = None
        self.validator_pool = ThreadPoolExecutor(max_workers=2)

    def start(self):
        logger.info('Scheduler starts...')
        self.feed_providers()

        self.worker_process = Process(target=fetch_ips, args=(self.worker_queue, self.validator_queue))
        self.validator_thread = Thread(target=validate_ips, args=(self.validator_queue, self.validator_pool))

        self.worker_process.start()
        self.validator_thread.start()

    def feed_providers(self):
        logger.debug('feed_providers...')
        self.worker_queue.put(CoolProxyProvider())
        self.worker_queue.put(FreeProxyListProvider())
        self.worker_queue.put(KuaidailiProvider())

    def stop(self):
        self.worker_queue.close()
        self.worker_process.terminate()
        self.validator_thread.terminate()
