from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('allauth.urls')),
    path('signup', views.signup_view.as_view(), name='signup_view'),
    path('login', views.login_view.as_view(), name='login_view'),
    path('friends', views.friendList.as_view(), name='friends'),
    path('talk_room/<int:pk>', views.talk_room.as_view(), name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('change', views.change_view, name='change_view'),
    path('changeDone', views.changeDone_view.as_view(), name='changeDone_view'),
    path('passwordChange', views.passwordChange_view.as_view(), name='passwordChange_view'),
    path('passwordChangeDone', views.passwordChangeDone.as_view(), name='passwordChangeDone_view'), 
    path('logout', views.logout_view.as_view(), name='logout_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)