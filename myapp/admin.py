from django.contrib import admin
from .models import CustomUser, Friend, TalkRoom
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class FriendAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'friend')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(TalkRoom)