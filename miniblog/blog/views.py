from django.shortcuts import render, HttpResponseRedirect
from .forms import Signupform, Loginform, Postform
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import Post
from django.contrib import messages
from django.contrib.auth.models import Group
# Create your views here.

# Home Page
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

# About Page
def about(request):
    return render(request, 'blog/about.html')

# Contact Page
def contact(request):
    return render(request, 'blog/contact.html')

# Dashboard Page
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts, "full_name": full_name, "groups":gps})
    else:
        return HttpResponseRedirect('/login')

# Logout
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

# Login Page 
def login(request):
    if not request.user.is_authenticated:   
        if request.method == "POST":
            form = Loginform(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    auth_login(request,user)
                    messages.success(request, "Congratulations ! You Have Successfully Login !!! ")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = Loginform()
        return render(request,'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


# Signup Page
def signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulation ! You have become an Author ")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = Signupform()
    return render(request, 'blog/signup.html', {'form':form})

# Add New Post Page
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Postform(request.POST)
            if form.is_valid():
                messages.success(request, "You Add Data Successfully ! ")
                utitle = form.cleaned_data['title']
                udesc = form.cleaned_data['desc']
                pst = Post( title = utitle, desc= udesc )
                pst.save()
                form = Postform()
        else:
            form= Postform()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login')
    
# Update Post Page
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                messages.success(request, "You Updated Data Successfully ! ")
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request,'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login')

# Delete Post Page
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pid = Post.objects.get(pk=id)
            pid.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login')