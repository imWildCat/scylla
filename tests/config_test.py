from scylla.config import set_config, get_config, batch_set_config


def test_config():
    set_config('foo', 'bar')
    config_str = get_config('foo')
    assert 'bar' == config_str


def test_config_default():
    config_str = get_config('empty', default='baz')
    assert 'baz' == config_str


def test_batch_set(mocker):
    m = mocker.patch('scylla.config.set_config')
    batch_set_config(**{'a': 1, 'b': 2})
    m.assert_called()
