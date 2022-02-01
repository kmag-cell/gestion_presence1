from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Registre, Apprenant
from django.contrib.auth.models import User

class LearnerInline(admin.StackedInline):
    model = Apprenant
    extra = 1


class LearnerAdmin(UserAdmin):
    inlines = (LearnerInline,)

class RegistreAdmin(admin.ModelAdmin):
    fields = ('apprenant', 'arrivee')
    list_display = ('apprenant', 'date', 'arrivee', 'depart', 'temps')
    list_filter = [
        "apprenant",
        "date",
        "depart",
        "temps"
    ]




# # Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, LearnerAdmin)
admin.site.register(Registre, RegistreAdmin)
admin.site.register(Apprenant)
