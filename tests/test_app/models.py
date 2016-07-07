from django.db import models


class RelatedModel(models.Model):
    test_field = models.IntegerField()


class BaseModel(models.Model):
    fk = models.ForeignKey(RelatedModel)


class MultiFieldRelatedModel(models.Model):
    test_field_0 = models.IntegerField()
    test_field_1 = models.IntegerField()


class MultiFieldModel(models.Model):
    fk = models.ForeignKey(MultiFieldRelatedModel)


# Models for testing fields passed to constructor

class DefaultModel(models.Model):
    test_field_0 = models.IntegerField(default=0, blank=True)
    test_field_1 = models.IntegerField()


class DefaultBaseModel(models.Model):
    fk = models.ForeignKey(DefaultModel)


class NullModel(models.Model):
    test_field_0 = models.IntegerField(null=True, blank=True)
    test_field_1 = models.IntegerField()


class NullBaseModel(models.Model):
    fk = models.ForeignKey(NullModel)