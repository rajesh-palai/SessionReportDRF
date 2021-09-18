from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.generics import RetrieveAPIView
from .models import UserSession,CustomUser
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.utils import timezone

class RegisterAPI(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer2 = RegisterSerializer(data= request.data)
        serializer2.is_valid(raise_exception=True)
        logintime= serializer2.data['start_time']
        if timezone.now() > logintime:
            login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Create your views here.

from django.contrib.sessions.models import Session
from datetime import datetime

class SessionReportView(RetrieveAPIView):
        queryset = CustomUser.objects.all()
        serializer_class = RegisterSerializer
        session_started = Session.usersession.session_start

        session_duration = datetime.now() - session_started
