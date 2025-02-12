from django.db import models

# Create your models here.

class User(models.Model):

    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=254)
    passwordHash = models.CharField(max_length=254) # Hashed using Argon2 algorithm
    phoneNumberPrefix = models.IntegerField() # Ex: +1 -> US, +505 -> Nicaragua
    phoneNumber = models.CharField(max_length=10) # No parenthesis or dashes included
    
    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return f"{self.username} | {self.email}"

    def get_absolute_url(self):
        return reversed("User_detail", kwargs={"pk": self.pk})

class Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=254)
    streetAddress = models.CharField(max_length=254)
    streetAddressLine2 = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    state = models.CharField(max_length=254)
    zipCode = models.CharField(max_length=10) # XXXXX[-XXXX] zipCode length = 5 + extended 4 digits.
    
    class Meta:
        verbose_name = ("Address")
        verbose_name_plural = ("Addresses")

    def __str__(self):
        return f"{self.user.username} | {self.streetAddress}"

    def get_absolute_url(self):
        return reversed("Address_detail", kwargs={"pk": self.pk})

