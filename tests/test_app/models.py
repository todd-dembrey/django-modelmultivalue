from django.db import models


class RelatedModel(models.Model):
    test_field = models.IntegerField()


class BaseModel(models.Model):
    fk = models.ForeignKey(RelatedModel)
