from django.contrib import admin
from . import models as contests_models

admin.site.register(contests_models.Contest)
