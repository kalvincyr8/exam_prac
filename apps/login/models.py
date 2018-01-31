from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
# Create your models here.
# class PokeManager(models.Manager):

class UserManager(models.Manager):
    def loginVal(self, post_data):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = post_data['email'])

        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(post_data['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results

    def creator(self, post_data):
        user = self.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            email = post_data['email'],
            password = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt()),
            dob = post_data['dob']
        )

        return user

    def validate(self, post_data):
        results = {'status': True, 'errors':[]}
        if len(post_data['first_name']) < 2:
            results['errors'].append('First Name needs to be at least 2 charcters long.')
            results['status'] = False
        if len(post_data['last_name']) < 2:
            results['errors'].append('Last Name needs to be at least 2 charcters long.')
            results['status'] = False
        if not re.match("[^@]+@[^@]+\.[^@]+", post_data['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False
        if post_data['password'] != post_data['password_confirm']:
            results['errors'].append('passwords do not match.')
            results['status'] = False

        if len(post_data['password']) < 8:
            results['errors'].append('passwords must be at least 8 charcters.')
            results['status'] = False

        if len(self.filter(email = post_data['email'])) > 0:
            results['errors'].append('User already exsits.')
            results['status'] = False

        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
            results['errors'].append('Names must be charcters only.')
            results['status'] = False

        return results


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField(verbose_name=None)
    objects = UserManager()
