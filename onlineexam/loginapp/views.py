from django.db import connection
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth

from examapp.models import Question
from loginapp.models import Myuser
# Create your views here.



def giveMePage1(request):
    return render(request,'loginapp/addition.html')

def login(request):
    if request.method=="GET":
        return render(request,'loginapp/login.html')
    else:
        uname = (request.POST['username'])
        password = (request.POST['password'])
        userobj=auth.authenticate(username=uname,password=password)
        print(uname)
        print(password)
        print(userobj)
        if userobj==None:
            return render(request,'loginapp/login.html',{'message':'invalid credentials!'})
        else:
            auth.login(request,userobj)
            queryset=Question.objects.all().values('subject').distinct()
            querysets=list(queryset)
            # queryset=Question.objects.all()
            print(f'subjects from db are:- {querysets}')
            print(connection.queries)
            request.session['username']=userobj.username
            request.session['score']=0
            request.session['qindex']=0
            request.session['duration']=11
            request.session['answer']={}
            if(userobj.is_superuser==0):
                userid = userobj.id 
                myuserobj = Myuser.objects.filter(user_ptr_id=userid)
                print(f"myuserobj is {myuserobj}")
                imgsrc = myuserobj[0].imagepath
                # print(imgsrc[0].imagepath)
                return render(request,'examapp/subject.html',{'message':'Successfully loggedIn! Start Test','subjects':querysets,'imgsrc':imgsrc})
            else:
                return render(request,'examapp/admindashboard.html')
            
    
def saveUser(request):
    if request.method=='GET':
        return render(request,'loginapp/register.html')
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    img = request.FILES['photo'] 
    imagepath = '/upload/'+img.name
    print(imagepath)
    with open('loginapp/static/'+imagepath, 'wb+')as destination:
        for chunk in img.chunks():
            destination.write(chunk)
    userobj = Myuser.objects.create_user(username=username, password=password, email=email, imagepath=imagepath)
    # userobj=User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
    userobj.save()
    return render(request,'loginapp/login.html',{'message':'registration successfully!'})
