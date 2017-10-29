from django.contrib import admin
from .models import *

@admin.register(Contest)
class ProblemAdmin(admin.ModelAdmin):
    exclude = ('completed', )
