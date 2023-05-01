from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.contrib.auth.decorators import login_required
from .models import *
from better_profanity import profanity
import random
import requests
import json

# Create your views here.
@login_required(login_url='login')
def home(request):
    obs = Post.objects.all()[::-1]
    for j in obs:
        print(j.img)
        params = {
            'models': 'nudity-2.0,offensive',
            'api_user': '859734078',
            'api_secret': 'jn9HYrYETXgejxkQ72WU'
            }
        #imgPath='C:/Users/chaya/projects/blog/media/{}'.format(j.img)
        imgPath='https://web-production-e9de.up.railway.app/media/{}'.format(j.img)
        files = {'media': open(imgPath, 'rb')}
        r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

        output = json.loads(r.text)
        print(output)
        if output['offensive']['prob'] > 0.5 or output['nudity']['sexual_activity'] > 0.5 or output['nudity']['sexual_display'] > 0.5 or output['nudity']['erotica'] > 0.5:
            print('Offensive content detected !')
            j.img = '/images/no_image_available.jpg'

    l=['Travel','Photography','Technology','Music','Study','Science','Sports','Business','Fashion','Public','Others']
    d={}
    for i in range(len(l)):
        ob = Post.objects.filter(category=l[i])
        d[l[i]] = len(ob)
    return render(request, 'home.html', context={'obs': obs,'dict':d})

@login_required(login_url='login')
def profile(request,val):
    objs = Post.objects.filter(name=val)
    objs2 = User.objects.get(username=val)
    return render(request, 'profile.html', context={'objs': objs, 'objs2': objs2})

@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        img = request.FILES.get('img',False)
        print(type(img))
        
        if not img:
            img = 'images/no_image_available.jpg'
        
        category = request.POST['Categories']
        name = request.POST['name']

        print(title,body,img,name,category)
        profanity.load_censor_words()
        title = profanity.censor(title)
        body = profanity.censor(body)
        ob = Post(title=title,body=body,img=img,category=category,name=name)
        ob.save()
        return redirect('home')

    else:
        return render(request, 'create.html')

@login_required(login_url='login')
def edit(request,val):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        img = request.FILES.get('img',False)
        if not img:
            img = 'images/no_image_available.jpg'
        category = request.POST['Categories']
        
        obj = Post.objects.get(id=val)
        obj.title=title
        obj.body=body
        obj.img=img
        obj.category=category
        obj.save()
        print("hi")
        return redirect('home')
    else:
        obj = Post.objects.get(id=val)
        return render(request, 'edit.html', context={'obs': obj})

@login_required(login_url='login')
def delete(request,val):
    ob = Post.objects.get(id=val).delete()
    return redirect('home')

@login_required(login_url='login')
def search(request):
    obstitle=Post.objects.filter(title__icontains=request.GET['query'])
    obsbody=Post.objects.filter(body__icontains=request.GET['query'])
    obs=obstitle.union(obsbody)
    return render(request,'search.html',context={'obs':obs, 'query':request.GET['query']})

@login_required(login_url='login')
def category(request,val):
    objs = Post.objects.filter(category=val)
    return render(request, 'category.html', context={'obs': objs, 'obs2': val})

def readmore(request,val):
    obj = Post.objects.get(id=val)
    temp = Comment.objects.filter(value=val)
    ob = list(Post.objects.all())
    random_item = random.sample(ob,3)
    return render(request,'readmore.html', context={'obs':obj, 'temps':temp, 'random_item':random_item})

def cmt(request):
    if request.method == 'POST':
        body = request.POST['comment']
        name = request.POST['name']
        value = request.POST['value']
        profanity.load_censor_words()
        body = profanity.censor(body)
        ob = Comment(body=body,name=name,value=value)
        ob.save()

        return redirect('readmore',value)
    else:
        return redirect('readmore',value)

@login_required(login_url='login')
def about(request):
    obs = Post.objects.all()
    obs2 = User.objects.all()
    return render(request, 'about.html', context={'obs': obs, 'obs2':obs2})