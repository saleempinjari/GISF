from django.shortcuts import render
from .models import MyAppUsers
from .PasswordManage import decrypt,encrypt

#Customized New User Creation
def NewUserCreate(request):
    password = request.POST.get('pwd')
    username = request.POST.get('uid')
    if request.method == "POST":
        encr = encrypt(password,username)
        MyAppUsers.objects.create(username=username, password=encr)
        dec = decrypt(encr, username)

    return render(request,'MyAdmin/register.html')

# Ddjango Defined New Register Form

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

def register(request):
    form = UserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])

            return render(request = request,
                          template_name = "MyAdmin/newuser.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "MyAdmin/newuser.html",
                  context={"form":form})

def loginView(request):
    if request.method=='GET':
        return render(request, 'MyAdmin/login.html', {})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None :
            login(request, user)
            #return redirect('mainmenu/')
            return render(request, 'MyAdmin/mainmenu.html', {})
        else:
            return render(request, 'MyAdmin/login.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'MyAdmin/logout.html', {})

def homepage(request):
    return render(request, 'MyAdmin/home.html', {})

def about(request):
    return render(request,'MyAdmin/About.html')

from django.contrib.auth.decorators import login_required
@login_required(login_url='/MyAdmin/clogin/')
def mainmenu(request):
    return render(request, 'MyAdmin/mainmenu.html', {})