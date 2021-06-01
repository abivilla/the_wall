from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    return render (request,'login.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')

    context={
        "posts": Post.objects.all(),
        "comments":Comment.objects.all()
    }

    return render (request,'success.html', context)

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for error in errors.values():
                messages.error(request,error)
            return redirect('/')

 
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
     
    
    user = User.objects.create(first_name=request.POST['first_name'],last_name = request.POST['last_name'],email = request.POST['email'], password=pw_hash) 
    
    request.session["user_id"] = user.id
    request.session["user_name"] = user.first_name
    return redirect('/wall')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email)

        if user: 
            logged_user = user[0] 
       
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
           
                request.session['user_id'] = logged_user.id
                request.session["user_name"] = logged_user.first_name
            
                return redirect('/wall')
            else:
                messages.error(request,"This password is incorrect!")
                return redirect('/')
        else:
            messages.error(request,"This User doesn't exist!")
            return redirect('/')
    
    return redirect('/')

def logout(request):
    request.session.flush()

    return redirect('/')

def create_post(request):

    poster = User.objects.get(id=request.session["user_id"])

    Post.objects.create(message=request.POST["post"],poster=poster)

    return redirect('/wall')

def create_comment(request,id):

    poster = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    
    Comment.objects.create(comment=request.POST["comment"],poster=poster,post=post)

    return redirect('/wall')
