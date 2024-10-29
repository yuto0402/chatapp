from django.contrib import admin
from .models import CustomUser, TalkRoom
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

admin.site.register(TalkRoom)