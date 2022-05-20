import pytest
import requests


class ApiClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="/", params=None, headers=None):
        url = f"{self.base_address}{path}"
        return requests.get(url=url, params=params, headers=headers)

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        return requests.post(url=url, params=params, data=data, json=json, headers=headers)

    def put(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        return requests.put(url=url, params=params, data=data, json=json, headers=headers)


@pytest.fixture
def dog_api():
    return ApiClient(base_address="https://dog.ceo/api/")


@pytest.fixture
def openbrewerydb_api():
    return ApiClient(base_address="https://api.openbrewerydb.org/")


@pytest.fixture
def jsonplaceholder_api():
    return ApiClient(base_address="https://jsonplaceholder.typicode.com/")


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="https://ya.ru",
        help="This is request url"
    )

    parser.addoption(
        "--status_code",
        default="200",
        #        choices=["200", "300", "400", "404", "500", "502"],
        help="This is request code"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def code(request):
    return request.config.getoption("--status_code")
