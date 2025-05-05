from io import BytesIO
from django.core.files import File
from PIL import Image, ImageOps, ImageChops, ImageColor
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from threading import Thread

# Create your models here.

def create_sku():
    return str(max(int(product.sku) for product in Product.objects.all())+1).zfill(4)

class Product(models.Model):
    sku = models.CharField(max_length=4, primary_key=True, default=create_sku, blank=False)
    name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    stock = models.IntegerField(default=0)

    def price_in_dollars(self):
        return round(self.price / 100.0, 2)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"SKU {self.sku} | {self.name}"

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    end_x = models.IntegerField()
    end_y = models.IntegerField()
    texture_mask = models.ImageField(blank=True, null=True)
    color_mask = models.ImageField(blank=True, null=True)
    
    # Overwritten save method to generate texture mask on model save
    def save(self):
        product_image_data = self.image.read()
        product_image_io = BytesIO(product_image_data)
        product_image = Image.open(product_image_io).convert('RGBA')
        
        start = (int(product_image.size[0] * self.start_x/100), int(product_image.size[1] * self.start_y/100))
        end = (int(product_image.size[0] * self.end_x/100), int(product_image.size[1] * self.end_y/100))
        
        texture_mask_Image = product_image.crop((start[0], start[1], end[0], end[1]))
        
        django_image_io = BytesIO()
            
        texture_mask_Image.convert('RGB').save(django_image_io, format='JPEG', optimize=True)
        
        djangoImageFile = File(django_image_io, f'{self.product.name}_texture_mask.jpg')
        
        self.texture_mask.save(f'{self.product.name}_texture_mask.jpg', djangoImageFile, save=False)
        
        super().save()
        
        product_image_io.close()
        django_image_io.close()
        # start color combinations task

        print('making color combinations')
        background_job = Thread(target=ProductColor.createColoredProducts, args=[self])
        background_job.start()
        

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField()
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
    
class ProductPreview(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.ImageField()
    
    class Meta:
        verbose_name = "Produt Preview"
        verbose_name_plural = "Product Previews"

    def __str__(self):
        return f"{self.product.product.name} | {self.design.name} | {self.color.name}"

    def get_absolute_url(self):
        return reversed("Product_preview", kwargs={"pk": self.pk})
    
class ProductColor(models.Model):
    productImage = models.ForeignKey(ProductImage, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    
    @staticmethod
    def createColoredProducts(productImage: ProductImage):
        for color in Color.objects.all():
            new_ProductColor = ProductColor(productImage=productImage, color=color)
            new_ProductColor.save()
    
    def save(self):
        
        # productImageData = self.productImage.image.read()
        # productImageIO = BytesIO(productImageData)
        productImage = Image.open(self.productImage.image).convert('RGBA')
        
        # colorMaskImageData = self.productImage.color_mask.read()
        # colorMaskImageIO = BytesIO(colorMaskImageData)
        try:
            colorMaskImage = Image.open(self.productImage.color_mask).convert('RGBA')
            
            color_hex = self.color.hexValue
            color = (
                int(color_hex[:2], 16),
                int(color_hex[2:4], 16),
                int(color_hex[4:], 16)
            )
            
            colorMaskProduct = Image.composite(Image.new('RGBA', colorMaskImage.size, color), colorMaskImage, colorMaskImage)
            colorMask = Image.new('RGBA', productImage.size, color='white')

            colorMask.paste(colorMaskProduct, colorMaskImage)

            colorPreviewImage = ImageChops.multiply(productImage, colorMask)

            imageFile = BytesIO()
            colorPreviewImage.convert('RGB').save(imageFile, 'JPEG', optimize=True, quality=60)
            self.image.save(f'{self.productImage.product.name}_{self.color.name}.png', File(imageFile), save=False)
        except ValueError:
            self.image = self.productImage.image
        
        super().save()
