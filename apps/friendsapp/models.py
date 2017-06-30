# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..log_regis.models import Users


class friendsManager(models.Manager):
    def addFriend(self, Users):
        pass

class friends(models.Model):
    owner_id=models.ForeignKey(Users, related_name='users')
    user_id=models.ForeignKey(Users, related_name='friend_id')
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=friendsManager()
