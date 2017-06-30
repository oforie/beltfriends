# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from .models import friends, Users

# Create your views here.
def index(request):
    user = Users.objects.filter(id=request.session['id'])
    name = user[0].name
    print user[0].id
    all_users= Users.objects.exclude(name=name)
    # myfriends = friends.objects.all(user_id=user[0].id)

    context = {'name':name, 'everybody':all_users}
    return render(request, 'friendsapp/index.html', context)

def others(request, id):
    if id:
        user = Users.objects.filter(id=id)
    context = { 'id': id, 'user':user[0]}
    return render(request, 'friendsapp/others.html', context)

def addtoFriends(request):
    if request.POST:
        print request.POST['addfriend']
        friends.objects.create(owner_id=request.session['id'], user_id=request.POST['addfriend'])
        results = friends.objects.filter(id=request.POST['addfriend'])
        if results:
            print results[0]
        print 'added to friends'
        return redirect(reverse('friends:index'))


def logout(request):
    request.session.flush()
    return redirect(reverse('auth:index'))


# def addFriend(request):
    