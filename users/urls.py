from django.urls import path

from users.views import UserListCreateView, RetrieveUpdateDestroyAPIView

urlpatterns = [
    path('user/', UserListCreateView.as_view(), name="list-register-user"),
    path('my-profile/', RetrieveUpdateDestroyAPIView.as_view(), name="retrieve-update-delete-user"),
]