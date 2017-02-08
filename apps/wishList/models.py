from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from ..login.models import User

# Create your models here.
class WishListManager(models.Manager):
    def user_items(self, u_id):
        print u_id
        print '<--------in user_items function'
        user = User.objects.get(id=u_id)
        print user.first_name, '<--------- user object first name$$$$$$$$$'
        user_list = WishList.objects.filter(user__id=u_id)
        # user_list = User.objects.filter(items_added__id=u_id)
        print user_list, '<---------here is my list object of items by user_id'
        # print user_list[0].user.first_name, '<-----first name'
        return user_list

    def all_items(self, u_id):
        print u_id
        print '<--------in all_items function'
        # u_id = User.objects.get(id=u_id)
        all_items = self.exclude(user__id=u_id)
        print all_items, '<---------here are all the items created by other people'
        return all_items

    def new_item(self, data, u_id):
        errors = []
        if len(data['item']) < 1:
            errors.append('Please enter a valid item')
        if not len(data['item']) > 3:
            errors.append('Please enter a valid item')
        else:
            user = User.objects.get(id=u_id)
            item = data['item']
            print item, '<-------item'

            print user, '<------------ user object'
            print user.id, '<----------- user id', user.first_name, '<------ user name'
            try:
                item_match = self.get(item=item)
                errors.append('Item already exists')
                return(False, errors)
            except:
                user_id = user.id
                item_added = WishList.objects.create(item=item, created_by=user)
                item_added.user.add(user) #accessing the itermediary table to add the user object to the wishlist object
                # user.items_added.add(item_added) accessing the itermediary table to add the wishlist object to the user object
                print item_added, '<------- item added'
                return (True, item_added)
        if errors:
            print 'So MANY ERRORS!!!!'
            return(False, errors)

    def list_update(self, u_id, i_id):
        print '^^^^^^^^^^ in the list_update method ^^^^^^^'
        print i_id, '<-------item', u_id, "<--------user"
        messages = []
        try:
            user = User.objects.get(id=u_id)
            print user
            item = self.get(id=i_id)
            print item
            item.user.add(user)
            print item.user.all(), '<<<<<<<<<<<<<<<<<<-------------- this is all user objects'
            print user.items_added.all(), 'THIS SHOULD BE ITEM OBJECTS!!!!!!!'
            messages.append('You have successfully added this item to your list')
            return(True, messages, item)
        except:
            messages.append('Error: Item not added to your list')
            return(False, messages)

    def item_remove(self, i_id, u_id):
        messages = []
        try:
            user = User.objects.get(id=u_id)
            item = self.get(id=i_id)
            item.user.remove(user)
            messages.append('You have successfully removed this item')
            return(True, messages)
        except:
            messages.append('Item could not be removed')
            return(False, messages)


    def item_delete(self, i_id, u_id):
        errors = []
        try:
            item = self.get(id=i_id)
            if item.created_by.id == u_id:
                item.delete()
                errors.append('You have successfully deleted this item.')
                return(True, errors)
            else:
                errors.append('You do not have authority to delete this item.')
                return (False, errors)
        except:
            pass


class WishList(models.Model):
    user = models.ManyToManyField(User, related_name='items_added') #connected to the user table with a hidden key of items_added.  this represents all of the items that this user has added to a wishlist
    item = models.CharField(max_length=45)
    created_by = models.ForeignKey(User, related_name='items_created') #connected wishlist table with a hidden key of items_created to list
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = WishListManager()
