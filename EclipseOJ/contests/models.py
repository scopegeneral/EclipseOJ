from django.db import models

class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    def __str__(self):
        return 'Contest '+str(self.id)
