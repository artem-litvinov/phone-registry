from django.db import models


class RegistryEntry(models.Model):
    code = models.IntegerField()
    min_number = models.IntegerField()
    max_number = models.IntegerField()
    capacity = models.IntegerField()
    operator = models.TextField()
    region = models.TextField()

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(name="phone_number", fields=["code", "min_number", "max_number"]),
        ]
