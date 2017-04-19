from django.contrib import admin
from .models import Profile, Relationship

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    select_related = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)
