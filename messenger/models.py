from django.db import models

class Hook(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    data = models.TextField()
    type = models.CharField(blank=True, null=True, max_length=10)

    def __str__(self):
        return "{}".format(self.date)