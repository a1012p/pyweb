from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import myUser
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    con_delete = False


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

admin.site.register(myUser,CustomUserAdmin)
# Register your models here.

