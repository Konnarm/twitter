from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from model_utils.models import TimeStampedModel


class TwitterUser(TimeStampedModel):
    twitter_id = models.IntegerField(verbose_name=_('twitter id'))
    twitter_handle = models.CharField(verbose_name=_('twitter handle'), max_length=256)
    followers_ids = ArrayField(models.IntegerField(), verbose_name=_('followers ids'))
