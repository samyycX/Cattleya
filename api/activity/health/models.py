from django.db import models


class Health(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    last_heartrate = models.FloatField()
    last_updated_time = models.DateTimeField()