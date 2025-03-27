from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Design, Size, Color

ORDER_STATUS_CHOICES = [
    ("PL", "Placed"),
    ("PR", "Processing"),
    ("SH", "Shipped"),
    ("CO", "Completed")
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
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
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("OrderItem")
        verbose_name_plural = ("OrderItems")

    def __str__(self):
        return f"{self.quantity} | {self.product.name} | {self.design.name}"

    def get_absolute_url(self):
        return reversed("OrderItem_detail", kwargs={"pk": self.pk})
