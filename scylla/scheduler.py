from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process
from threading import Thread

from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip
from scylla.providers import BaseProvider
from scylla.worker import Worker
from .providers import CoolProxyProvider, FreeProxyListProvider, KuaidailiProvider


def fetch_ips(q: Queue, validator_queue: Queue):
    print('fetch_ips...')
    worker = Worker()

    while True:
        provider: BaseProvider = q.get()
        print('get new provider:', provider.__class__.__name__)

        for url in provider.urls():
            html = worker.get_html(url)
            proxies = provider.parse(html)
            validator_queue.put(proxies)


def validate_ips(q: Queue, validator_pool: ThreadPoolExecutor):
    print('validate_ips...')
    proxies: [ProxyIP] = q.get()

    for p in proxies:
        validator_pool.submit(validate_proxy_ip, p=p)


class Scheduler(object):

    def __init__(self):
        self.worker_queue = Queue()
        self.validator_queue = Queue()
        self.worker_thread = None
        self.validator_thread = None
        self.validator_pool = ThreadPoolExecutor(max_workers=5)

    def start(self):
        print('Scheduler starts...')
        self.feed_providers()

        self.worker_thread = Process(target=fetch_ips, args=(self.worker_queue, self.validator_queue))
        self.validator_thread = Thread(target=validate_ips, args=(self.validator_queue, self.validator_pool))

        self.worker_thread.start()
        self.validator_thread.start()

    def feed_providers(self):
        print('feed_providers...')
        self.worker_queue.put(CoolProxyProvider())
        self.worker_queue.put(FreeProxyListProvider())
        self.worker_queue.put(KuaidailiProvider())
