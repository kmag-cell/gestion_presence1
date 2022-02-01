from django.shortcuts import render, redirect
from .forms import ApprenantForm
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .backEnd import FaceRecognition
from .models import Apprenant
import datetime
import geocoder

facerecognition = FaceRecognition()

def home(request):
    return render(request, 'home/home.html')


def register(request):
    if request.POST:
        form = ApprenantForm(request.POST or None)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    apprenant = Apprenant.objects.get(user_id=user.id)
                    date = datetime.date.today()
                    registre_day = apprenant.registre_set.filter(date=date).count()
                    if registre_day == 0:
                        now = datetime.datetime.now().strftime('%H:%M:%S')
                        apprenant.registre_set.create(arrivee=now)
                    return redirect('/home/login')

                else:
                    messages.error(request, 'Compte désactivé', extra_tags='alert alert-error alert-dismissible show')
            else:

                messages.error(request, 'Les identifiants que vous avez saisis sont incorrects !', extra_tags='alert alert-error alert-dismissible show')

        else:

            return HttpResponse('Données incorrects')

    form = ApprenantForm()
    context = {
        'title' : 'Register Form',
        'form' : form
    }
    return render(request, 'home/register.html', context)


def login(request):
    user_id = facerecognition.recognizeFace()
    print(user_id)
    return redirect('/home/welcome/' + str(user_id))


def welcome(request, user_id):
    user_id = int(user_id)
    print(user_id)
    data = {
        'user': Apprenant.objects.get(user_id=user_id)
    }

    return render(request,'home/profile.html', data)


def logout(request):
    logout(request)
    return redirect('home/login')

def adresse_ip(request):
    wifi_adress = '105.235.111.211'
    g = geocoder.ip("me")
    ip = g.geojson['features'][0]['properties']['ip']
    print(ip)
    if wifi_adress == ip:
        loc = g.geojson['features'][0]['geometry']['coordinates']
        return loc
    else:
        return None


def dashboard(request):
    locate = adresse_ip(request)
    user = request.user
    date = datetime.date.today()
    apprenant = Apprenant.objects.get(user_id=user.id)
    registre = apprenant.registre_set.filter(date=date)[0]
    if locate:
        print(locate)
        return render(request, 'map.html', {'locate': locate, 'registre': registre, 'user': user})
    else:
        messages.error(request, "Vous n'êtes pas à la fabrique", extra_tags='alert alert-error alert-dismissible show')
        return redirect('home:login')



def signer(request):
    user = request.user
    date = datetime.date.today()
    try:
        apprenant = Apprenant.objects.get(user_id=user.id)
        registre = apprenant.registre_set.filter(date=date)[0]
    except Apprenant.DoesNotExist:
        pass
    else:
        if registre.depart is None:
            now = datetime.datetime.now().strftime('%H:%M:%S')
            registre.depart = now
            registre.save()
        else:
            deactivate = True
        return redirect(reverse('home:dashboard'),{'deactivate': deactivate})



