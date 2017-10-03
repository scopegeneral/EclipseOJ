from django.contrib import admin
from .models import Problem, TestCase

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    exclude = ('problem_ID', )

admin.site.register(TestCase)
