from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Profile,Music,Category,Comment,Follow,Item


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
# Register your models here.
admin.site.register(Profile)
admin.site.register(Music)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Item, MyModelAdmin)
