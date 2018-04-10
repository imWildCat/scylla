import pytest
from requests_html import HTML

from scylla.providers import BaseProvider


def test_base_provider_method_urls():
    base_provider = BaseProvider()

    with pytest.raises(NotImplementedError):
        base_provider.urls()


def test_base_provider_method_parse():
    base_provider = BaseProvider()

    with pytest.raises(NotImplementedError):
        base_provider.parse(HTML(html='<html></html>'))


def test_to_string():
    base_provider = BaseProvider()

    assert base_provider.__str__() == 'BaseProvider'


def test_should_render_js():
    base_provider = BaseProvider()

    assert base_provider.should_render_js() is False
