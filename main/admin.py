from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = UserAdmin.list_display + ('time_zone',)

    def time_zone(self, obj):
        return UserProfile.objects.get(user_id=obj.id).time_zone

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
