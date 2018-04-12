import logging


def test_basic_logging(caplog):
    caplog.set_level(logging.INFO)
    logging.info('foo')
    assert 'foo' in caplog.text
