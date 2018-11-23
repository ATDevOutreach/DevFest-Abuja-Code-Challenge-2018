from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name='account', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    phone = models.IntegerField(null=True)

    def recharge(self, amount):
        """ Recharges User account """
        self.balance = self.balance + amount
        self.save()

    def deduct(self, amount):
        """ Deducts amount from user account """

        self.balance = self.balance - amount
        self.save()
    
    def can_make_transaction(self, amount):
        """ checks if a user can make a transaction """
        return self.balance >= amount


@receiver(post_save, sender=User)
def create_account(sender, **kwargs):
    if kwargs['created']:
        user_account = Account.objects.get_or_create(
            user=kwargs['instance']
        )


class Activity(models.Model):
    ACTIONS = (
        ('RC', 'Account TopUp'),
        ('SM', 'Send SMS'),
        ('AR', 'Airtime Recharge'),
    )
    STATUS = (
        ('P', 'PENDING'),
        ('S', 'SUCCESS'),
        ('F', 'FAILED')
    )

    action = models.CharField(choices=ACTIONS, max_length=2)
    status = models.CharField(choices=STATUS, max_length=1)
    user = models.ForeignKey(
        User, related_name='activities', on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


def success(user, action, description=None):
    """ Create a success Activity """

    return Activity.objects.create(user=user, action=action, description=description, status='S')


def failed(user, action, description=None):
    """ Create a failed Activity """
    return Activity.objects.create(user=user, action=action, description=description, status='F')


def pending(user, action, description=None):
    """ Create a pending Activity """
    return Activity.objects.create(user=user, action=action, description=description, status='P')
