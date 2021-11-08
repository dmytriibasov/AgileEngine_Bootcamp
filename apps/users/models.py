from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


# Create your models here.
class User(AbstractUser):
    """
    Redefined default Django UserModel. Username field is not required anymore, only email instead.
    """
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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = CustomUserManager()

    def __str__(self):
        return self.email

