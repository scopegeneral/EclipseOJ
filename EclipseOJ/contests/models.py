from django.db import models

class Contest(models.Model):
    contest_ID = models.IntegerField()
    phase_choices = (
        ('B' , 'BEFORE'),
        ('C' , 'RUNNING'),
        ('P' , 'PENDING_SYSTEM_TEST'),
        ('S' , 'SYSTEM_TEST'),
        ('F' , 'FINISHED')
    )
    phase = models.CharField(max_length=2,choices=phase_choices)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return str(self.contest_ID)
