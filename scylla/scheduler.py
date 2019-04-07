import time
import queue
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from multiprocessing import Queue, Process
from threading import Thread

import pyppeteer
import schedule

from scylla.config import get_config
from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip
from scylla.loggings import logger
from scylla.providers import *
from scylla.worker import Worker

FEED_FROM_DB_INTERVAL_MINUTES = 30

def fetch_ips(q: Queue, validator_queue: Queue, run_once=False):
    logger.debug('worker_process started.')
    logger.info('fetching ips...')
    worker = Worker()

    while True:
        try:
            if run_once and q.empty():
                raise SystemExit
                break

            provider: BaseProvider = q.get()

            provider_name = provider.__class__.__name__

            logger.info('Get a provider from the provider queue: ' + provider_name)

            for url in provider.urls():

                html = worker.get_html(url, render_js=provider.should_render_js())

                if html:
                    proxies = provider.parse(html)

                    for p in proxies:
                        validator_queue.put(p)
                        # logger.debug('Put new proxy ip into queue: {}'.format(p.__str__()))

                    logger.info(
                        ' {}: feed {} potential proxies into the validator queue'.format(provider_name, len(proxies))
                    )
        except (KeyboardInterrupt, InterruptedError, SystemExit):
            worker.stop()
            break
        except pyppeteer.errors.PyppeteerError as e:
            logger.error("""pyppeteer.errors.PyppeteerError detected: %s\n
                         'Please make sure you have installed all the dependencies for chromium correctly""", e)
            break

    logger.debug('worker_process exited.')

def validate_ips(validator_queue: Queue, validator_pool: ThreadPoolExecutor, run_once=False):
    logger.debug('validator_thread started.')

    while True:
        try:
            ## wait 5 mins for next proxy ip in run once mode
            proxy: ProxyIP = validator_queue.get(timeout=300 if run_once else None)

            validator_pool.submit(validate_proxy_ip, p=proxy)
        except (KeyboardInterrupt, SystemExit):
            break
        except queue.Empty:
            logger.debug('validator_thread has timed out.')
            break

    logger.debug('validator_thread exited.')

    validator_pool.shutdown(wait=True)
    logger.debug('validator_pool exited.')


def cron_schedule(scheduler, run_once=False):
    """
    :param scheduler: the Scheduler instance
    :param run_once: flag for testing
    """

    def feed():
        scheduler.feed_providers()

    def feed_from_db():

        # TODO: better query (order by attempts)
        proxies = ProxyIP.select().where(ProxyIP.updated_at > datetime.now() - timedelta(days=14))
        for p in proxies:
            scheduler.validator_queue.put(p)

        logger.info('Feed {} proxies from the database for a second time validation'.format(len(proxies)))

    # feed providers at the very beginning
    scheduler.feed_providers()

    schedule.every(10).minutes.do(feed)
    schedule.every(FEED_FROM_DB_INTERVAL_MINUTES).minutes.do(feed_from_db)

    logger.debug('cron_thread started.')

    # After 1 minute, try feed_from_db() for the first time
    wait_time_for_feed_from_db = 1 if run_once else 60
    time.sleep(wait_time_for_feed_from_db)
    feed_from_db()

    while True:
        try:
            schedule.run_pending()

            if run_once:
                raise SystemExit
            else:
                time.sleep(60)
        except (KeyboardInterrupt, InterruptedError, SystemExit):
            break

    logger.debug('cron_thread exited.')


class Scheduler(object):

    def __init__(self):
        self.worker_queue = Queue()
        self.validator_queue = Queue()
        self.worker_process = None
        self.validator_thread = None
        self.cron_thread = None
        self.validator_pool = ThreadPoolExecutor(max_workers=int(get_config('validation_pool', default='31')))

    def start(self, run_once=False):
        """
        Start the scheduler with processes for worker (fetching candidate proxies from different providers),
        and validator threads for checking whether the fetched proxies are able to use.
        :param daemon: if False, scheduler will run each task only once then exit when they all finish
        """
        self.cron_thread = Thread(target=cron_schedule, args=(self, run_once), daemon=True)
        self.worker_process = Process(target=fetch_ips, args=(self.worker_queue, self.validator_queue, run_once))
        self.validator_thread = Thread(target=validate_ips, args=(self.validator_queue, self.validator_pool, run_once))

        self.cron_thread.daemon = True
        self.worker_process.daemon = True
        self.validator_thread.daemon = True

        self.cron_thread.start()
        self.worker_process.start()
        self.validator_thread.start()

    def join(self):
        """
        Wait for worker processes and validator threads
        """
        try:
            if self.cron_thread and self.cron_thread.is_alive():
                self.cron_thread.join()
            if self.worker_process and self.worker_process.is_alive():
                self.worker_process.join()
            if self.validator_thread and self.validator_thread.is_alive():
                self.validator_thread.join()
        except (KeyboardInterrupt, SystemExit):
            pass

    def feed_providers(self):
        logger.debug('feed {} providers...'.format(len(all_providers)))

        for provider in all_providers:
            self.worker_queue.put(provider())

    def stop(self):
        self.worker_queue.close()
        self.worker_process.terminate()
        # self.validator_thread.terminate() # TODO: 'terminate' the thread using a flag
        self.validator_pool.shutdown(wait=False)

    def is_alive(self):
        return (self.cron_thread and self.cron_thread.is_alive()) or \
            (self.worker_process and self.worker_process.is_alive()) or \
            (self.validator_thread and self.validator_thread.is_alive())
