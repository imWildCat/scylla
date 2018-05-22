import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue, Process
from threading import Thread

import schedule

from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip
from scylla.loggings import logger
from scylla.providers import *
from scylla.worker import Worker


def fetch_ips(q: Queue, validator_queue: Queue):
    logger.debug('fetch_ips...')
    worker = Worker()

    while True:
        try:
            provider: BaseProvider = q.get()

            provider_name = provider.__class__.__name__

            logger.debug('Get a provider from the provider queue: ' + provider_name)

            for url in provider.urls():

                html = worker.get_html(url)

                if html:
                    proxies = provider.parse(html)

                    for p in proxies:
                        validator_queue.put(p)
                        logger.debug('Put new proxy ip into queue: {}'.format(p.__str__()))

                    logger.info(
                        ' {}: feed {} potential proxies into the validator queue'.format(provider_name, len(proxies))
                    )
        except (KeyboardInterrupt, InterruptedError, SystemExit):
            logger.info('worker_process exited.')
            break


def validate_ips(q: Queue, validator_pool: ThreadPoolExecutor):
    while True:
        try:
            proxy: ProxyIP = q.get()

            validator_pool.submit(validate_proxy_ip, p=proxy)
        except KeyboardInterrupt:
            break


def cron_schedule(scheduler, only_once=False):
    """

    :param scheduler: the Scheduler instance
    :param only_once: flag for testing
    """
    def feed():
        scheduler.feed_providers()

    # feed providers at the very beginning
    scheduler.feed_providers()

    schedule.every(10).minutes.do(feed)

    logger.info('Start python scheduler')

    flag = True

    while flag:
        try:
            schedule.run_pending()

            if only_once:
                flag = False
            else:
                time.sleep(60)
        except (KeyboardInterrupt, InterruptedError):
            logger.info('Stopping python scheduler')
            break


class Scheduler(object):

    def __init__(self):
        self.worker_queue = Queue()
        self.validator_queue = Queue()
        self.worker_process = None
        self.validator_thread = None
        self.cron_thread = None
        self.validator_pool = ThreadPoolExecutor(max_workers=20)

    def start(self):
        """
        Start the scheduler with processes for worker (fetching candidate proxies from different providers),
        and validator threads for checking whether the fetched proxies are able to use.

        """
        logger.info('Scheduler starts...')

        self.cron_thread = Thread(target=cron_schedule, args=(self,), daemon=True)
        self.worker_process = Process(target=fetch_ips, args=(self.worker_queue, self.validator_queue))
        self.validator_thread = Thread(target=validate_ips, args=(self.validator_queue, self.validator_pool))

        self.cron_thread.daemon = True
        self.worker_process.daemon = True
        self.validator_thread.daemon = True

        self.cron_thread.start()
        self.worker_process.start()  # Python will wait for all process finished
        logger.info('worker_process started')
        self.validator_thread.start()
        logger.info('validator_thread started')

    def join(self):
        """
        Wait for worker processes and validator threads

        """
        while (self.worker_process and self.worker_process.is_alive()) or (
                self.validator_thread and self.validator_thread.is_alive()):
            self.worker_process.join()
            self.validator_thread.join()

    def feed_providers(self):
        logger.debug('feed_providers...')
        self.worker_queue.put(SpyMeProvider())
        self.worker_queue.put(CoolProxyProvider())
        self.worker_queue.put(FreeProxyListProvider())
        self.worker_queue.put(KuaidailiProvider())
        self.worker_queue.put(XiciProvider())
        self.worker_queue.put(Data5uProvider())

    def stop(self):
        self.worker_queue.close()
        self.worker_process.terminate()
        # self.validator_thread.terminate() # TODO: 'terminate' the thread using a flag
        self.validator_pool.shutdown(wait=False)
