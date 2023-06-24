from django.contrib import admin
from . models import CustomUser,Problem,Report,Comment

admin.site.register(CustomUser)
admin.site.register(Problem)

admin.site.register(Report)
admin.site.register(Comment)