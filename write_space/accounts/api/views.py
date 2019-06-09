from rest_framework.generics import (ListAPIView,RetrieveAPIView
,RetrieveUpdateAPIView,RetrieveDestroyAPIView,CreateAPIView)

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from rest_framework.permissions import (AllowAny,IsAuthenticated,IsAdminUser
,IsAuthenticatedOrReadOnly)
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
# from .permissions import IsOwnerOrReadOnly

from django.contrib.auth import get_user_model
User = get_user_model()

from . import serializers

# from .pagination import postLimitOffsetPagination,postPageNumberPagination


class userCreateApiView(CreateAPIView):
    serializer_class = serializers.userCreateSerializer
    queryset = User.objects.all()


class userLoginApiView(APIView):
    serializer_class = serializers.userLoginSerializer
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = serializers.userLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
