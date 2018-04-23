from scylla.cli import main


def test_cli(mocker):
    # batch_set_config_func = mocker.patch('scylla.app_config.batch_set_config')
    scheduler_start = mocker.patch('scylla.scheduler.Scheduler.start')
    # create_db_tables = mocker.patch('scylla.database.create_db_tables')

    ret = main(['-no-ws'])

    assert 0 == ret

    # batch_set_config_func.assert_called_once() # FIXME: assert not called but actually called
    # create_db_tables.assert_called_once() # FIXME: assert not called but actually called
    scheduler_start.assert_called_once()
