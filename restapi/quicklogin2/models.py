

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

class CustomUser(AbstractUser):

    objects = models.Manager
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)

    def __str__(self):
        return self.email

class SessionRecord(models.Model):

    login_count= models.IntegerField(blank=True)
    logout_count= models.IntegerField(blank=True)
    attendance= models.BooleanField



class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)

    session_start = models.DateTimeField(auto_now_add=True)

    @receiver(user_logged_in)
    def register_session(sender, user, request, **kwargs):

        request.session.save()

        UserSession.objects.get_or_create(
            user=user,
            session=Session.objects.get(pk=request.session.session_key)
        )