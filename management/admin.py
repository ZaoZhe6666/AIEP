from django.contrib import admin

# Register your models here.
from .models import Attack_method, runSubmit

admin.site.register(Attack_method)
admin.site.register(runSubmit)