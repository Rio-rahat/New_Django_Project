from django.shortcuts import render
from Login_app import models, forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    data={}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = models.userInfo.objects.get(user__pk=user_id)
        data={
            'title':'Index Page',
            'user_basic_info': user_basic_info,
            'user_more_info': user_more_info
        }
    return render(request, 'Login_app/index.html', data)

def register(request):
    registered = False
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        user_info_form = forms.UserInfoForm(data=request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']
            user_info.save()

            registered = True
                
    else:
        user_form = forms.UserForm()
        user_info_form = forms.UserInfoForm()
        
    data = {
        'title':'Register Page',
        'user_form': user_form,
        'user_info_form': user_info_form,
        'registered': registered
    }
    return render(request, 'Login_app/register.html', data)

def login_page(request):
    data = {
        'title':'Login Page'
    }
    return render(request, 'Login_app/login.html', data)

def user_login(request):
    data={
        'title': 'Login Page'
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('Login_app:index'))
            else:
                return HttpResponse("Account is not Active!!!")
        else:
            return HttpResponse("Login Details Are Wrong!!!")
    
    else:
        return render(request, 'Login_app/login.html', data)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_app:index'))