from django.contrib import admin
from .models import Post, Profile


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
