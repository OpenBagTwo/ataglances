"""Tests for Glances webserver interfacing functionality"""
from pathlib import Path

import pytest
import requests
import yaml

from ataglances import glance


class TestRequestData:

    def test_unavailable_server_raises_connection_error(self):
        with pytest.raises(requests.ConnectionError):
            glance.request_data('tchaikovsky', 'all')

    def test_non_json_endpoint_raises_value_error(self, requests_mock):
        requests_mock.get('http://tchaikovsky:61208/api/3/hello', text='Hello world!')
        with pytest.raises(ValueError):
            glance.request_data('tchaikovsky', 'hello')

    def test_request_data_returns_dict(self, requests_mock):
        requests_mock.get('http://tchaikovsky:61208/api/3/demo', json={'hello': 'world'})

        assert glance.request_data('tchaikovsky', 'demo') == {'hello': 'world'}

    def test_request_data_can_hit_different_endpoints(self, requests_mock):
        requests_mock.get('http://tchaikovsky:61208/api/3/demo', json={'hello': 'world'})
        requests_mock.get('http://tchaikovsky:61208/api/3/status', json={'how u doin': 'im fine'})

        assert glance.request_data('tchaikovsky', 'status') == {'how u doin': 'im fine'}

    def test_request_data_can_use_different_ports(self, requests_mock):
        requests_mock.get('http://tchaikovsky:12345/api/3/demo', json={'sup': 'universe'})
        requests_mock.get('http://tchaikovsky:61208/api/3/demo', json={'hello': 'world'})

        assert glance.request_data('tchaikovsky', 'demo', port=12345) == {'sup': 'universe'}

    def test_request_data_only_supports_the_v3_api(self):
        with pytest.raises(NotImplementedError, match='only supports the Glances v3 API'):
            glance.request_data('tchaikovsky', 'demo', api_version=2)

    def test_request_data_passes_timeout_to_requests(self, monkeypatch):

        timeout_values = []

        class MockResponse:
            def json(self):
                return {}

        def patched_get(*args, **kwargs):
            timeout_values.append(kwargs.get('timeout'))
            return MockResponse()

        monkeypatch.setattr(requests, 'get', patched_get)

        glance.request_data('tchaikovsky', 'demo')
        glance.request_data('tchaikovsky', 'demo', timeout=1.7)

        assert timeout_values == [0.5, 1.7]


def load_sample_data():
    samples = {}
    for filename in Path(__file__).parent.joinpath('sample_responses').glob('*.yaml'):
        samples[Path(filename).stem] = yaml.safe_load(Path(filename).open(mode='r'))
    return samples


SAMPLE_DATA = load_sample_data()


class TestConvertListResponseToDict:

    @pytest.mark.parametrize('sample_name', list(SAMPLE_DATA.keys()))
    def test_smoketest(self, sample_name):
        glance.convert_list_response_to_dict(SAMPLE_DATA[sample_name])



