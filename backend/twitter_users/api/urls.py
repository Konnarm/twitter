from django.urls import path

from .views import UserFollowersRetrieveView

urlpatterns = [
    path(
        "get_followers/<str:handle>/",
        UserFollowersRetrieveView.as_view(),
        name="followers",
    ),
    path(
        "get_followers/<str:handle>/<int:followers_slice>/",
        UserFollowersRetrieveView.as_view(),
        name="followers",
    ),
]
