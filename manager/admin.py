from django.contrib import admin

# 添加manager在http://localhost/admin界面中可见
from .models import manager

admin.site.register(manager)
