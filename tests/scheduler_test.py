from scylla.validator import Validator


# def test_validate_job(mocker):
#     mocker.patch('scylla.validator.Validator.validate')
#     v = Validator('127.0.0.1', 80)
#     validate_job(v)
#     v.validate.assert_called_once()

# FIXME: cannot patch Queue.get
# def test_validate_ips(mocker):
#     with patch.object(Queue, 'get', return_value=None) as mock_get:
#         validate_ips(Queue(), ThreadPoolExecutor(max_workers=1))
#
#     mock_get.assert_called_once()

# mocker.patch('multiprocessing.Queue.get')
# mocker.patch('concurrent.futures.ThreadPoolExecutor.submit')
# validate_ips(Queue(), ThreadPoolExecutor(max_workers=1))
# Queue.get.assert_called_once()
