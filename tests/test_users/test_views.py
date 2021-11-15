import pytest
from fixtures import user_data, setup_user

from rest_framework.reverse import reverse
from rest_framework.test import APIClient


from apps.users.models import User


client = APIClient()


@pytest.mark.django_db
class TestUser:

    def test_signup_view(self, user_data):

        assert User.objects.all().count() == 0

        data = user_data
        response = client.post(reverse('users:signup'), data=data)

        assert response.status_code == 201
        assert User.objects.all().count() == 1
        assert response.data['email'] == 'dmytriiii@mail.com'

        data['password2'] = 'ChangedPassword'
        response = client.post(reverse('users:signup'), data=data)

        assert response.status_code == 400

    def test_login_view(self, setup_user, user_data):

        assert User.objects.all().count() == 1

        login_data = {'email': user_data['email'], 'password': user_data['password']}
        response = client.post(reverse('users:login'), data=login_data)

        assert response.status_code == 200

        login_data = {'email': 'another_email', 'password': 'AnotherPassword'}
        response = client.post(reverse('users:login'), data=login_data)

        assert response.status_code == 401
