from django.contrib import admin

from .models import User, SavedJob

# Register your models here.

admin.site.register(User)
admin.site.register(SavedJob)