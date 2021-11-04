from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):

    username = None

    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    def __str__(self):
        return self.email
