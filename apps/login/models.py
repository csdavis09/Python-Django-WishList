from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def new_user(self, data):
        errors = []
        print data
        print '9'*50

        if len(data['first_name']) < 3:
            errors.append('Please enter a valid First Name')
        # elif not data['first_name'].isalpha():
        #     errors.append('Please enter a valid First Name')

        if len(data['last_name']) < 3:
            errors.append('Please enter a valid Last Name')
        # elif not data['last_name'].isalpha():
        #     errors.append('Please enter a valid Last Name')

        if len(data['user_name']) < 3:
            errors.append('Please enter a User Name')

        if len(data['email']) < 1:
            errors.append('Please enter your email')
        elif not re.match(EMAIL_REGEX, data['email']):
            errors.append('Please enter a valid Email address')
        else:
            u_email = data['email']
            try:
                User.objects.get(u_email=email)
                errors.append('Email already exists.  Please enter a valid email or login.')
            except:
                pass

        if len(data['password'].encode()) < 8:
            errors.append('Password must be at least 8 characters')
        elif not data['password'].encode() == data['pw_confirm'].encode():
            errors.append('Passwords do not match! Please enter matching passwords')

        if errors:
            return(False, errors)
        else:
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            pw_confirm = data['pw_confirm'].encode()
            pw_hash = bcrypt.hashpw(pw_confirm, bcrypt.gensalt())
            u = User.objects.create(first_name=first_name, last_name=last_name, email=email, pw_hash=pw_hash)
            u.save()
            return(True, u)

    def login(self, data):
        errors = []
        pw = data['password'].encode()
        email = data['email']
        print '<--------- in the login function'
        if len(email) < 1:
            errors.append('Please enter your email')
        elif not re.match(EMAIL_REGEX, email):
            errors.append('Please enter a valid email')
        else:
            try:
                u = User.objects.get(email = email)
                if len(pw) < 8:
                    errors.append('Invalid password')
                elif not bcrypt.hashpw(pw, u.pw_hash.encode()) == u.pw_hash:
                    errors.append('Invlaid password')
            except User.DoesNotExist:
                errors.append('Please register before logging in')

        if errors:
            print '***** So Many ERRORS!!!!!******'
            return(False, errors)
        else:
            return(True, u)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()
