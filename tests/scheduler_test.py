import pytest

from scylla.scheduler import Scheduler


@pytest.fixture
def scheduler():
    return Scheduler()


def test_start(mocker, scheduler):
    feed_providers = mocker.patch('scylla.scheduler.Scheduler.feed_providers')
    process_start = mocker.patch('multiprocessing.Process.start')
    thread_start = mocker.patch('threading.Thread.start')

    scheduler.start()

    feed_providers.assert_called_once()
    process_start.assert_called_once()
    thread_start.assert_called_once()


def test_feed_providers(mocker, scheduler):
    pass
    # TODO: mock Queue.put or find other solutions
    # queue_put = mocker.patch('multiprocessing.Queue.put')
    #
    # scheduler.feed_providers()
    #
    # queue_put.assert_called()
