from django.db import models

class Hook(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    data = models.TextField()

    def __str__(self):
        return "{}".format(self.date)