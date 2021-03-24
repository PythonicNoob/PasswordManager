from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass

# Create your models here.
class Website(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    URL = models.URLField()
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)