import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def auth_request(user_data):
    request_factory = APIRequestFactory()
    request = request_factory.request()
    request.force_authenticate(user_data)
    return {'request': request}
