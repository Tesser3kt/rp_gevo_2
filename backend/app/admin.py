from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "cls")

    def full_name(self, obj):
        return obj.user.get_full_name()
