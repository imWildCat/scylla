import argparse
import sys

from scylla.config import batch_set_config, get_config
from ._version import __version__

CMD_DESCRIPTION = """Scylla command line mode
This command could start a scheduler for crawling and validating proxies.
In addition, a web server with APIs can also be launched.

"""


def main(args) -> int:
    parser = argparse.ArgumentParser(description=CMD_DESCRIPTION,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--no-webserver', '-no-ws', action='store_true',
                        help='Prevent starting a web server for JSON API')
    parser.add_argument('--web-port', '-wp', type=int, default=8899,
                        help='The port number for the web server')
    parser.add_argument('--web-host', '-wh', type=str, default='0.0.0.0',
                        help='The hostname for the web server')
    parser.add_argument('--skip-scheduler', action='store_true',
                        help='Prevent the scheduler from crawling')
    parser.add_argument('--scheduler-run-once', action='store_true',
                        help='Run all tasks in scheduler only once')
    parser.add_argument('--version', '-v', action='store_true',
                        help='Print the version of Scylla')
    parser.add_argument('--db-path', type=str, default='./scylla.db',
                        help='The sqlite database file location')
    parser.add_argument('--validation-pool', type=int, default=31,
                        help='The validation pool size (i.e. the limit of concurrent validation tasks for proxies)')
    parser.add_argument('--no-forward-proxy-server', action='store_true',
                        help='Disable the forward proxy server')
    parser.add_argument('--proxy-port', '-pp', type=int, default=8081,
                        help='The port number for the forward proxy')

    parsed_args = parser.parse_args(args)

    parsed_args_dict = vars(parsed_args)

    batch_set_config(**vars(parsed_args))

    handle_special_flags(parsed_args_dict)

    from scylla.database import create_db_tables
    from scylla.loggings import logger
    from scylla.scheduler import Scheduler
    from scylla.web import start_web_server_non_blocking
    from scylla.proxy import start_forward_proxy_server_non_blocking

    create_db_tables()

    s = Scheduler()

    try:
        # scheduler
        if not get_config('skip_scheduler'):
            run_once = bool(get_config('scheduler_run_once'))
            logger.info('Start scheduler, run_once=%s' % run_once)
            s.start(run_once)

        # forward proxy serveer
        if not get_config('no_forward_proxy_server'):
            logger.info('Start forward proxy server')
            p_web = start_forward_proxy_server_non_blocking()

        # web server
        if not get_config('no_webserver'):
            logger.info('Start web server')
            p_proxy = start_web_server_non_blocking(workers=1)

        # exit
        if s.is_alive():
            s.join()
            logger.info('scheduler done.')
        if p_web:
            p_web.join()
        if p_proxy:
            proxy.join()

    except (KeyboardInterrupt, SystemExit):
        logger.info('catch KeyboardInterrupt, exiting...')
        s.stop()
        sys.exit(0)

    logger.info('scylla exiting...')
    return 0


def handle_special_flags(args: dict):
    if args['version']:
        print('v{}'.format(__version__))
        sys.exit(0)


def app_main():
    sys.exit(main(sys.argv[1:]))
