from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('music',views.post,name='post'),
    path('create/profile/<int:id>',views.create_profile, name='create-profile'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('api/profiles/', views.ProfileList.as_view()),
    path('category/',views.category,name='category'),
    path('musics_list/<int:id>',views.musics_list,name='musics_list'),
    path('music_delete/<int:id>',views.music_delete,name='music_delete'),
    path('music_update/<int:id>',views.music_update,name='music_update'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/<to_follow>', views.follow, name='follow'),
    path('video/',views.video, name='video'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
