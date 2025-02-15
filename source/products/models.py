from django.db import models
from django.urls import reverse
from users.models import User

# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=50)
    imageURL = models.URLField()
    price = models.IntegerField()
    description = models.TextField()

    def price_in_dollars(self):
        return round(self.price / 100.0, 2)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"SKU {self.sku} | {self.name}"

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.URLField()
    dateUploaded = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = "Design"
        verbose_name_plural = "Designs"

    def __str__(self):
        return f"{self.user.username} | {self.name} | {self.dateUploaded}"

    def get_absolute_url(self):
        return reversed("Design_detail", kwargs={"pk": self.pk})
    
class Color(models.Model):
    hexValue = models.CharField(max_length=6)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return f"#{self.hexValue.upper()} | {self.name}"

    def get_absolute_url(self):
        return reversed("Color_detail", kwargs={"pk": self.pk})

    
class Size(models.Model):
    productType = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    printableWidth = models.IntegerField()
    printableHeight = models.IntegerField()

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return f"{self.productType.name} | {self.name}"

    def get_absolute_url(self):
        return reversed("Size_detail", kwargs={"pk": self.pk})


class DesignedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "DesignedProduct"
        verbose_name_plural = "DesignedProducts"

    def __str__(self):
        return f"{self.user} | {self.color.name} {self.size.name} {self.product.name} | {self.design.name}"

    def get_absolute_url(self):
        return reversed("DesignedProduct_detail", kwargs={"pk": self.pk})
