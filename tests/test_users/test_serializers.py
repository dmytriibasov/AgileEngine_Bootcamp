import pytest
from apps.users.serializers import SignUpSerializer


@pytest.mark.django_db
def test_signup_serializer_validation():
    data = {
        'email': 'dmytriiii@mail.com',
        'password': 'PassWord777',
        'password2': 'PassWord777',
        'first_name': 'dmytrii',
        'last_name': 'test',
        'birth_date': '2018-02-04'
    }
    serializer = SignUpSerializer(data=data)
    assert serializer.is_valid()
    serializer.save()

    serializer = SignUpSerializer(data=data)
    assert not serializer.is_valid()
