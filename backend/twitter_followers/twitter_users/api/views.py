from rest_framework.generics import RetrieveAPIView

from .serializers import SecondLineFollowersSerializer
from ..models import SecondLineFollowersCounter
from ..tasks import get_second_line_followers_task


class UserFollowersRetrieveView(RetrieveAPIView):
    serializer_class = SecondLineFollowersSerializer

    def get_object(self):
        handle = self.kwargs.get("handle")
        if handle:
            handle = handle.strip()
        second, created = SecondLineFollowersCounter.objects.get_or_create(screen_name=handle)
        get_second_line_followers_task.delay(handle, self.kwargs.get("followers_slice", False))
        return second
