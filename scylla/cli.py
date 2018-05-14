import argparse
import sys

from scylla.config import batch_set_config
from scylla.database import create_db_tables
from scylla.loggings import logger
from scylla.scheduler import Scheduler
from scylla.web import start_web_server

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

    parsed_args = parser.parse_args(args)

    parsed_args_dict = vars(parsed_args)

    batch_set_config(**vars(parsed_args))

    create_db_tables()

    s = Scheduler()

    try:
        s.start()

        # web server
        if not parsed_args_dict['no_webserver']:
            logger.info('Start the web server')
            start_web_server(
                host=parsed_args_dict['web_host'], port=parsed_args_dict['web_port'])

        s.join()
    except (KeyboardInterrupt, SystemExit):
        logger.info('catch KeyboardInterrupt, exiting...')
        s.stop()
        return 0

    return 0


def app_main():
    sys.exit(main(sys.argv[1:]))
