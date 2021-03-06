from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.db.models import Q


def control(request):
    return render(request,'control.html')





def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(content__icontains=query)

            results= Camera.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')


def setcookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie('java-tutorial', 'http://127.0.0.1:8001/')
    return response

def getcookie(request):
    tutorial  = request.COOKIES['java-tutorial']
    return HttpResponse("java tutorials @: "+  tutorial)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })





def destroy(request,id):
    camera = Camera.objects.get(id=id)
    camera.delete()
    return redirect('home')

def full(request,id):
    camera_data = Camera.objects.get(id=id)
    print(camera_data.id)
    camera = camera_data.ip
    camera_id = camera_data.id

    return render(request,'full.html',{'camera':camera,'camera_id':camera_data.id})


def add_camera(request):
    if request.method == "POST":
        camera = Camera()
        camera.ip = request.POST['ip']
        camera.name = request.POST['name']
        camera.save()
    else:
        return render(request,'add_camera.html')


    return render(request,'add_camera.html')

@login_required(login_url='login')
def home(request):
    username = request.user.username
    user_id = request.user.id
    print(user_id)
    print(username)

    camera = Camera.objects.all()


    return render(request,'home.html',{"camera":camera})

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error':'Username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                email = request.POST['email'])
                auth.login(request, user)
                return redirect('home')

        else:
            return render(request, 'signup.html', {'error':'Password doesn\'t matched'})

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error':'username or password is incorrect!'})

    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')