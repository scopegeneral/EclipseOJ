from django.contrib import admin
from . import models as discuss_models

admin.site.register(discuss_models.Post)
admin.site.register(discuss_models.Comment)
