import pytest
from rest_framework.exceptions import ValidationError
from fixtures import user_data
from apps.users.serializers import SignUpSerializer


@pytest.mark.django_db
def test_serializer():
    pass
