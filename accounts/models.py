import uuid
from django.db import models


class User(models.Model):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    email = models.EmailField(primary_key=True)
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    uid = models.CharField(max_length=40, default=uuid.uuid4)
    email = models.EmailField()
