from django.db import models
from users.models import User

# Create your models here.

class ProductType(models.Model):
    sku = models.CharField(max_length=10)
    name = models.CharField(max_length=254)

    class Meta:
        verbose_name = ("ProductType")
        verbose_name_plural = ("ProductTypes")

    def __str__(self):
        return f"SKU{self.sku} | {self.name}"

    def get_absolute_url(self):
        return reversed("ProductType_detail", kwargs={"pk": self.pk})

class ProductTemplate(models.Model):
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    sku = models.CharField(max_length=10)
    pricePerUnit = models.IntegerField() # Saved as Integer, formatted as float '.2f' on frontend
    attributes = models.JSONField() #different items may have different attributes
    imageURL = models.URLField()
    printableHeight = models.IntegerField() #in inches
    printableWidth = models.IntegerField() #in inches
    
    class Meta:
        verbose_name = ("ProductTemplate")
        verbose_name_plural = ("ProductTemplates")

    def __str__(self):
        return f"{self.productType.name} | {self.sku} @ {(self.pricePerUnit/100):.2f}"

    def get_absolute_url(self):
        return reversed("ProductTemplate_detail", kwargs={"pk": self.pk})

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField()

    class Meta:
        verbose_name = ("Design")
        verbose_name_plural = ("Designs")

    def __str__(self):
        return f"{self.user.username} | {self.image}"

    def get_absolute_url(self):
        return reversed("Design_detail", kwargs={"pk": self.pk})
    
class Product(models.Model):

    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    productTemplate = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    designWidth = models.IntegerField()
    designHeight = models.IntegerField()
    designPosX = models.IntegerField() # 0 to 100 as a percentage of the total printable area
    designPosY = models.IntegerField() # 0 to 100 as a percentage of the total printable area

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return f"{self.productTemplate.productType.name} | {self.design}"

    def get_absolute_url(self):
        return reversed("Product_detail", kwargs={"pk": self.pk})

