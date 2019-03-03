from rest_framework.serializers import ModelSerializer

from ..models import SecondLineFollowersCounter


class SecondLineFollowersSerializer(ModelSerializer):
    class Meta:
        model = SecondLineFollowersCounter
        fields = ("followers",)
