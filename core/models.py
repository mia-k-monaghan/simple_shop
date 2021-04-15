from django.db import models
from django.conf import settings
from localflavor.us.models import USStateField,USZipCodeField
# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, related_name="subscriptions")
    stripe_id = models.CharField(max_length=250,null=True)
    name = models.CharField(max_length=250, null=True,blank=True)
    active = models.BooleanField(default=False)
    fulfilled = models.BooleanField(default=False)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True)
    state = USStateField(null=True)
    zip = USZipCodeField(null=True)

    def __str__(self):
        return str(self.user)

class SingleOrder(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=250, null=True,blank=True)
    fulfilled = models.BooleanField(default=False)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True)
    state = USStateField(null=True)
    zip = USZipCodeField(null=True)

    def __str__(self):
        return str(self.email)
