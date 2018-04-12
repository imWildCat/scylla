import argparse
import sys

from scylla.config import batch_set_config
from scylla.scheduler import Scheduler


def main(args) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a')
    batch_set_config(**vars(parser.parse_args(args)))

    s = Scheduler()
    s.start()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
