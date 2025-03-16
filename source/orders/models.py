from django.db import models
from django.contrib.auth.models import User
from products.models import DesignedProduct

# Create your models here.

ORDER_STATUS_CHOICES = [
    ("PL", "Placed"),
    ("PR", "Processing"),
    ("SH", "Shipped")
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="customer")
    # address = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    subtotalCost = models.IntegerField(default=0)
    shippingCost = models.IntegerField(default=0)
    taxCost = models.IntegerField(default=0)
    totalCost = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default="PL")
    claim = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ("Order")
        verbose_name_plural = ("Orders")

    def __str__(self):
        return f"{self.user.username} | {self.date}"

    def get_absolute_url(self):
        return reversed("Order_detail", kwargs={"pk": self.pk})

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(DesignedProduct, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")

    def __str__(self):
        return f"{self.user} | {self.quantity} | {self.product}"

    def get_absolute_url(self):
        return reversed("OrderItem_detail", kwargs={"pk": self.pk})
