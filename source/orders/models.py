from django.db import models
from users.models import User
from products.models import Product

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    

    class Meta:
        verbose_name = ("CartItem")
        verbose_name_plural = ("CartItems")

    def __str__(self):
        return f"{self.user.username} | {self.quantity} | {self.product}"

    def get_absolute_url(self):
        return reversed("CartItem_detail", kwargs={"pk": self.pk})

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="customer")
    address = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField()
    subtotalCost = models.IntegerField()
    shippingCost = models.IntegerField()
    taxCost = models.IntegerField()
    totalCost = models.IntegerField()
    

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return f"{self.user.username} | {self.date}"

    def get_absolute_url(self):
        return reversed("Order_detail", kwargs={"pk": self.pk})

    
class OrderItem(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")

    def __str__(self):
        return f"{self.user} | {self.quantity} | {self.product}"

    def get_absolute_url(self):
        return reversed("OrderItem_detail", kwargs={"pk": self.pk})