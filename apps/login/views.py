from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    try:
        messages
    except:
        pass
    return render(request, 'login/index.html')

def process(request):
    if request.method == 'POST':
        if request.POST['process'] == 'register':
            add_user = User.objects.new_user(request.POST)
            if add_user[0] == False:
                messages.error(request, add_user[1])
                return redirect('login:login')
            else:
                # request.session['name'] = add_user[1].first_name
                request.session['id'] = add_user[1].id
                messages.success(request, 'Successfully registered!')
                return redirect('wishList:dashboard')

        elif request.POST['process'] == 'login':
            u_log = User.objects.login(request.POST)
            if u_log[0] == True:
                request.session['name'] = u_log[1].first_name
                request.session['id'] = u_log[1].id
                messages.success(request, 'Successfully logged in!')
                return redirect('wishList:dashboard')
            else:
                messages.error(request, u_log[1])
                return redirect('login:login')
        else:
            return redirect('login:login')

# def show(request):
#     return render(request, 'login/success.html')
#
# def logout(request):
#     request.session.clear()
#     return redirect('/')
