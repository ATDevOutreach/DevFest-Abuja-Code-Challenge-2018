from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.IntegerField()
    phone = models.IntegerField()

    def recharge(self, amount):
        """ Recharges User account """
        self.balance = self.balance + amount
        self.save()

    def deduct(self, amount):
        """ Deducts amount from user account """

        self.balance = self.balance - amount
        self.save()
