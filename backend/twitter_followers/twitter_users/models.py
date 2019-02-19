from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class BaseTwitterData(TimeStampedModel):
    screen_name = models.CharField(
        verbose_name=_("twitter handle"), max_length=256, null=True, unique=True
    )
    user_id = models.BigIntegerField(
        verbose_name=_("twitter id"), null=True, unique=True
    )

    class Meta:
        abstract = True


class TwitterUser(BaseTwitterData):
    followers_ids = ArrayField(
        models.BigIntegerField(), verbose_name=_("followers ids"), null=True
    )


class SecondLineFollowersCounter(BaseTwitterData):
    followers = JSONField(verbose_name=_("followers"), null=True)
