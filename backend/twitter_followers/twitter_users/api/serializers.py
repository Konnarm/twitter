from rest_framework.serializers import ModelSerializer

from ..models import SecondLineFollowersCounter


class SecondLineFollowersSerializer(ModelSerializer):
    """
    Serializer for second line followers, basically it just returns dict of followers {twitter_name: count}
    """

    class Meta:
        model = SecondLineFollowersCounter
        fields = ("followers",)
