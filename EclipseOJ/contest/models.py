from django.db import models

# Create your models here.
class Contest(models.Model):
    contest_id = models.IntegerField()
    phase_choices = (
        ('B' , 'BEFORE'),
        ('C' , 'RUNNING'),
        ('P' , 'PENDING_SYSTEM_TEST'),
        ('S' , 'SYSTEM_TEST'),
        ('F' , 'FINISHED')
    )
    phase = models.CharField(max_length=2,choices= phase_choices)
    contest_start = models.DateTimeField()
    contest_end = models.DateTimeField()
    def __str__(self):
        return str(self.contest_id)
