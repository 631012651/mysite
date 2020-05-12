from django.contrib import admin
from . import forms
# Register your models here.
from . import models
admin.site.register(models.User)
#admin.site.register(forms.UserForm)