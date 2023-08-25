from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.constants import USER_CREATED, USER_ALREADY_DELETED, USER_UPDATED_SUCCESSFULLY, USER_DELETED_SUCCESSFULLY
from users.models import User
from users.pagination import CustomPagination
from users.serializers import UserSerializer, UserRegistrationSerializer
from users.utils import current_time


class UserListCreateView(generics.ListCreateAPIView):
    """
    View to register user and list all users.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        Get request to list users.
        """
        page = self.paginate_queryset(self.get_queryset())
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({'data': serializer.data},
                        status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Post request to register user.
        """
        serializer = UserRegistrationSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        serializer.save(created_at=current_time())
        return Response({'data': serializer.data, 'message': USER_CREATED}, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update and delete user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Method to fetch logged in user
        """
        return self.request.user

    def put(self, request, *args, **kwargs):
        """
        Put request to update user profile
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_at=current_time())
        return Response({'data': serializer.data, 'message': USER_UPDATED_SUCCESSFULLY}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Delete request to inactive user profile
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': USER_DELETED_SUCCESSFULLY}, status=status.HTTP_204_NO_CONTENT)
