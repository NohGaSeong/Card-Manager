from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=16, unique=True)
    is_active = models.BooleanField(default=False)
    first_name = None
    last_name = None

    def __str__(self) -> str:
        return self.username

