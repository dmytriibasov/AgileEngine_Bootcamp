import pytest
from AgileEngine_Bootcamp.apps.users.serializers import SignUpSerializer


@pytest.mark.django_db
def test_signup_serializer():
    data = {'email': 'custom@email.com',
            'password': 'ProAdmin888',
            'password2': 'ProAdmin888'
            }
    serializer = SignUpSerializer(data=data)
    assert serializer.is_valid()
    serializer.save()

    serializer = SignUpSerializer(data=data)
    assert not serializer.is_valid()
