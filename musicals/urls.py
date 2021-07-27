from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('music',views.post,name='post'),
    
   
    path(r'^create/profile/$',views.create_profile, name='create-profile'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path(r'^api/profiles/$', views.ProfileList.as_view()),
    
    
    path('category/',views.category,name='category'),
    path('music_list/<int:id>',views.music_list,name='music_list'),
    path('music_delete/<int:id>',views.music_delete,name='music_delete'),
    path('music_update/<int:id>',views.music_update,name='music_update'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
