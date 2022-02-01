from django.db import models
from django.contrib.auth.models import User

class Apprenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name="Date de naissance", max_length=50)
    address = models.CharField(verbose_name="Lieu de residence",max_length = 100)
    formation = models.CharField(verbose_name="Formation",max_length = 15)
    phone = models.CharField(verbose_name="Contact",max_length = 10)
    startdate = models.DateField(verbose_name="Date entrée",max_length = 200)
    image=models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username + " (" + self.user.first_name + " " + self.user.last_name + ")"


class Registre(models.Model):
    apprenant=models.ForeignKey(Apprenant,on_delete=models.CASCADE)
    date=models.DateField(verbose_name="Date du jour", auto_now=True)
    arrivee = models.TimeField(verbose_name="Heure d'arrivée", auto_now=True, blank=True, null=True)
    depart = models.TimeField(verbose_name="Heure de départ", blank=True, null=True)
    temps = models.TimeField(verbose_name="Temps de travail", blank=True, null=True)

    def __str__(self):
        return self.apprenant.user.username
