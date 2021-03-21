from multiprocessing.spawn import freeze_support

from scylla.cli import app_main

if __name__ == '__main__':
    freeze_support()
    app_main()
