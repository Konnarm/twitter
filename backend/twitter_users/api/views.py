from rest_framework.generics import RetrieveAPIView

from .serializers import SecondLineFollowersSerializer
from ..helpers import get_second_line_followers


class UserFollowersRetrieveView(RetrieveAPIView):
    serializer_class = SecondLineFollowersSerializer

    def get_object(self):
        second = get_second_line_followers(
            self.kwargs.get("handle"), self.kwargs.get("followers_slice", False)
        )
        return second
