from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid


class EventModel(models.Model):
    client_uuid = models.UUIDField()
    account_uuid = models.UUIDField()
    event_type = models.CharField(max_length=20)
    body = JSONField()
    version = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
