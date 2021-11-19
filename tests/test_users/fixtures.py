import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from apps.users.models import User
from rest_framework.test import APIRequestFactory

client = APIClient()


@pytest.fixture
def user_data():
    data = {
        'email': 'dmytriiii@mail.com',
        'password': 'PassWord777',
        'password2': 'PassWord777',
        'first_name': 'dmytrii',
        'last_name': 'test',
        'birth_date': '2018-02-04'
    }
    return data


@pytest.fixture
def setup_user(user_data):
    user = client.post(reverse('users:signup'), data=user_data)
    return user


