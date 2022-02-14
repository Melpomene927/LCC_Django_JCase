from xml.dom import UserDataHandler
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
import user
from user.models import Profile
from user.forms import ProfileForm

# Create your views here.

# 個人資訊


def profile(request, id):
    user = Profile.objects.get(id=id)
    print(user)
    return render(request, './user/profile.html', {'user': user})


def user_login(request):
    if request.method == 'POST':
        # print('POST')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # print(user)
                login(request, user)
                return redirect('cases')
            else:
                print('Fail to login')
                if Profile.objects.filter(username=username).exists():
                    message = '密碼錯誤'
                else:
                    message = '帳號錯誤'
                print(message)

        except Exception as e:
            print(e)

        return render(request, './user/login.html', {'username': username, 'password': password, 'message': message})

    return render(request, './user/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')  # render(request, './user/lgoin.html')


def user_register(request):
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect(request, 'cases')

    return render(request, './user/register.html', {"form": form})
