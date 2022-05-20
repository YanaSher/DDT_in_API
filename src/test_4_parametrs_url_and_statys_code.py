import pytest
import requests


def test_url_status(base_url, code):
    response = requests.get(base_url)
    assert response.status_code == int(code)
