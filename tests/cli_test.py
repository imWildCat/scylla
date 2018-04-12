from scylla.cli import main


def test_cli(mocker):
    scheduler_start = mocker.patch('scylla.scheduler.Scheduler.start')
    batch_set_config = mocker.patch('scylla.config.batch_set_config')

    ret = main([])

    assert 0 == ret

    scheduler_start.assert_called_once()
    batch_set_config.assert_called_once()  # FIXME: assert not called but actually called
