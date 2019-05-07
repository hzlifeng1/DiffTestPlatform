from django.contrib import admin
from CodeDiff.models import ProjectInfo,ServerInfo,UserInfo

# Register your models here.
admin.site.register(ProjectInfo)
admin.site.register(ServerInfo)
admin.site.register(UserInfo)
