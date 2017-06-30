# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render, HttpResponse, redirect
from django.contrib import messages
from django.db import models
import re
import bcrypt


class UserManager(models.Manager):

    def registrations(self, postData):
        results={
            'status':True, 'errors':[], 'user':None
        }
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        password = postData['password']
        confirm_pw = postData['confirm_pw']
        dob = postData['dob']
        # for email format confirmation
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
       
        #  check length of first name
        if len(name) < 2:
            results['status']=False
            results['errors'].append('Name must be more than 2 characters')
            # check length of first name
        if len(alias) < 2:
            results['status']=False
            results['errors'].append('Alias must be more than 2 characters')
            # check email pattern
        if not re.match(regex, email):
            results['status']=False
            results['errors'].append('Please enter valid email')
            # check for matching password
        if password != confirm_pw:
            results['status']=False
            results['errors'].append('Please enter matching passwords')
            # checking password length
        if len(password)< 8:
            results['status']=False
            results['errors'].append('Password is too short')
        
        if len(dob)< 6:
            results['status']=False
            results['errors'].append('please enter a valid Birthday')

        # if no validation errors results['status'] stays True
        if results['status']:
            # querry for email in the database if it exists in the db, count > 
            if Users.objects.filter(email = email).count() > 0:
                results['errors'].append('email already in use')
                results['status'] = False

                # if not, write into db
            else:
                reg_password = postData['password']
                encoded_pw = reg_password.encode(encoding="utf-8", errors="strict")
                encrypted_pw = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
                print encoded_pw
                # addding new user to the database
                # Users.objects.all().delete()
                Users.objects.create(name=name, alias=alias, email=email, password = encrypted_pw, dob=dob)
                
                print postData['name'], 'has been successfully registered!'

                print Users.objects.all().count(), 'users are currently in your database'
                # user = Users.objects.get(email=email)
                # print results['user'][0].name, 'has been successfully registered!'
                # changing to results['user'] = user so we can take package our entire results object to views.py
                # results['user'] = user
                # results here represents the object which includes errors, user and status, accessible to views.py
        return results

            #login validations
    def login(self, postData):
        results={
            'status':True, 'errors':[], 'user':None
        }
        email = postData['email']
        password_input = postData['password']
        # clear previous users before running this code ( users.objects.all().delete())
        user = Users.objects.filter(email = email)
        
        if user:
            if bcrypt.hashpw(password_input.encode(), user[0].password.encode()) == user[0].password.encode():
                results['user'] = user
   
        else:
            results['status']=False
            results['errors'].append('Invalid login credentials')
        Users.objects.all().count(), 'users are currently in your database'
        return results
            
            
class Users(models.Model):
    name=models.CharField(max_length=30) 
    alias=models.CharField(max_length=30)
    email=models.CharField(max_length=45, unique=True)
    password=models.CharField(max_length=50)
    dob=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name + ','+ self.alias + ','+ str(self.id)

    objects=UserManager()