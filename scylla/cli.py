import argparse

from scylla.config import batch_set_config
from scylla.database import create_db_tables
from scylla.scheduler import Scheduler


def main(args) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a')

    batch_set_config(**vars(parser.parse_args(args)))

    create_db_tables()

    s = Scheduler()

    try:
        s.start()
    except KeyboardInterrupt:
        print('catch KeyboardInterrupt')
        s.stop()
        return 0

    return 0
