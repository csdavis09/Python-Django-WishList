from django.shortcuts import render, redirect
from .models import User, WishList
from django.contrib import messages

# Create your views here.
def login(request):
    return redirect('login:login')

def index(request):
    u_id = request.session['id']
    context = {
        'name': User.objects.get(id=u_id),
        'user_items': WishList.objects.user_items(u_id),
        'other_items': WishList.objects.all_items(u_id),
    }
    return render(request, 'wishList/index.html', context)
    #create a view page that lists all items in logged in user's wish list in a table
        #make a ORM call to pull all the items from the users list
    #can delete items that logged in user created
        #if user id for item matches the logged user, add button Delete
    #can remove items that logged in user added from others wish list
        #if user id doesn't match the userid for the item, add button Remove from my Wishlist
    #create a table with all the items from others wish lists

def show(request, id):
    users = User.objects.filter(items_added__id=id)
    print users, '<-----user object'
    item = WishList.objects.get(id=id)
    print item, '<-------item object'
    context = {
        'users': users,
        'item': item,
    }
    #lists a single item with a list of users who also have this item in their db
    return render(request, 'wishList/item.html', context)

def create(request):
    return render(request, 'wishList/new_item.html')

def add_item(request):
    if request.method == 'POST':
        u_id = request.session['id']
        add_item = WishList.objects.new_item(request.POST, u_id)
        print add_item, '<------- this was returned from .new_item'
        if add_item[0] == True:
            print '<___________ item added successfully'
            messages.success(request, 'Item successfully added')
        else:
            messages.error(request, add_item[1])
            return redirect('wishList:new_item')
    #validations when adding a new item: No Empty entries, should be more than 3 entries
    #should be added to the User's Wish list table
    #User should be redirected to dashboard return redirect('')
    return redirect('wishList:new_item')

def update_list(request, id):
    print '************ in the update_list function'
    u_id = request.session['id']
    u_list = WishList.objects.list_update(u_id, id)
    print u_list, '<---------------- updated list object'
    if u_list[0] == True:
        print u_list[1], '<---------- u_list[1]'
        print u_list[2], '<------------- item passed from models'
        for msg in u_list[1]:
            messages.success(request, msg)
        return redirect('wishList:dashboard')
    else:
        for msg in u_list[1]:
            messages.error(request, u_list[1])
    return redirect('wishList:dashboard')

def remove_item(request, id):
    u_id = request.session['id']
    i_remove = WishList.objects.item_remove(id, u_id)
    if i_remove[0] == True:
        for msg in i_remove[1]:
            messages.success(request, msg)
    else:
        for msg in i_remove[1]:
            messages.error(request, i_remove[1])
    return redirect('wishList:dashboard')

def delete_item(request, id):
    if request.method == 'POST':
        u_id = request.session['id']
        d_item = WishList.objects.item_delete(id, u_id)
        if d_item[0] == True:
            messages.success(request, d_item[1])
        else:
            messages.error(request, d_item[1])
    return redirect('wishList:dashboard')

def logout(request):
    request.session.clear()
    messages.success(request, 'You have successfully logged out')
    return redirect('login:login')
