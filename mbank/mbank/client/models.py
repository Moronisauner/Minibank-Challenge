from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class ClientModel(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_company = models.BooleanField('Empresarial?', blank=True, default=False)
