from django.contrib import admin
from .models import Product, ProductImage, Size, Design, Color, ProductPreview, ProductColor
from django.forms.models import BaseInlineFormSet
    
class ProductImageInlineFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        if index is not None and index >= 0:
            kwargs['initial'] = {
                'start_x': 30,
                'start_y': 30,
                'end_x': 70,
                'end_y': 70,
            }
        return kwargs

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageInlineFormSet
    extra = 0
    min_num = 1
    max_num = 1
    validate_min = True
    
class SizeInlineFormSet(BaseInlineFormSet):
    size_defaults = [
        {"name": "XS", "printableWidth": 1500, "printableHeight": 1700},
        {"name": "S",  "printableWidth": 1500, "printableHeight": 1800},
        {"name": "M",  "printableWidth": 1500, "printableHeight": 1800},
        {"name": "L",  "printableWidth": 1600, "printableHeight": 1800},
        {"name": "XL", "printableWidth": 1800, "printableHeight": 1900},
        {"name": "XXL","printableWidth": 1900, "printableHeight": 2100},
    ]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        if (
            getattr(self, 'is_adding', False) and
            index is not None and
            0 <= index < len(self.size_defaults)
        ):
            kwargs['initial'] = self.size_defaults[index]
        return kwargs
    
class SizeInline(admin.TabularInline):
    model = Size
    formset = SizeInlineFormSet
    extra = 6
    min_num = 1
    max_num = 6
    validate_min = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.is_adding = obj is None
        return formset
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, SizeInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and not obj.size_set.exists():
            default_sizes = [
                ('XS', 80, 100),
                ('S', 100, 120),
                ('M', 120, 140),
                ('L', 140, 160),
                ('XL', 160, 180),
                ('XXL', 180, 200),
            ]
            for name, width, height in default_sizes:
                Size.objects.create(
                    productType=obj,
                    name=name,
                    printableWidth=width,
                    printableHeight=height
                )

admin.site.register(Product, ProductAdmin)
admin.site.register([
    Design,
    Color,
    ProductColor,
    ProductPreview,
    ProductImage,
    Size
])
