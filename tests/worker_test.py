import typing
import pytest

from scylla.worker import Worker


@pytest.fixture
def worker_instance():
    return Worker()


def test_worker_initialization(worker_instance):
    worker = worker_instance
    assert worker.browser
    assert worker.requests_session


def test_get_html_without_js_rendering(worker_instance):
    worker: Worker = worker_instance
    result = worker.get_html('http://www.example.com/', render_js=False)

    if not result:
        assert False
    
    html: str = typing.cast(str, result.html())

    assert '<title>' in html
    assert '<head' in html
    assert '<body>' in html

# def test_get_html_with_js_rendering(worker_instance):
#     worker: Worker = worker_instance
#     html = worker.get_html('http://example.com/', render_js=True).html()
#     assert '<title>' in html
#     assert '<html' in html
#     assert '<body' in html  # Note: The actual body tag is `<body style="">`
