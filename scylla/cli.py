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
    parser.add_argument('--web-port', '-wp', type=int, default=8000,
                        help='The port number for the web server')
    parser.add_argument('--web-host', '-wh', type=str, default='0.0.0.0',
                        help='The hostname for the web server')
    parser.add_argument('--skip-scheduler', action='store_true',
                        help='Prevent the scheduler from crawling')
    parser.add_argument('--version', '-v', action='store_true',
                        help='Print the version of Scylla')
    parser.add_argument('--db-path', type=str, default='./scylla.db',
                        help='The sqlite database file location')

    parsed_args = parser.parse_args(args)

    parsed_args_dict = vars(parsed_args)

    batch_set_config(**vars(parsed_args))

    handle_special_flags(parsed_args_dict)

    from scylla.database import create_db_tables
    from scylla.loggings import logger
    from scylla.scheduler import Scheduler
    from scylla.web import start_web_server

    create_db_tables()

    s = Scheduler()

    try:
        if not get_config('skip_scheduler'):
            s.start()

        # web server
        if not get_config('no_webserver'):
            logger.info('Start the web server')
            start_web_server(
                host=parsed_args_dict['web_host'], port=parsed_args_dict['web_port'])

        s.join()
    except (KeyboardInterrupt, SystemExit):
        logger.info('catch KeyboardInterrupt, exiting...')
        s.stop()
        return 0

    return 0


def handle_special_flags(args: dict):
    if args['version']:
        print('v{}'.format(__version__))
        sys.exit(0)


def app_main():
    sys.exit(main(sys.argv[1:]))
