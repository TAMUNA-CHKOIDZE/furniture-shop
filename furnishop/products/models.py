from django.db import models
from django.utils.text import slugify

from products.choices import COLOR_CHOICES, MATERIAL_CHOICES


class Product(models.Model):
    category = models.ForeignKey(
        to='categories.Category',
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Category"
    )
    name = models.CharField(max_length=150, verbose_name="Product Name")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock Quantity")
    color = models.IntegerField(choices=COLOR_CHOICES, verbose_name="Color")
    material = models.IntegerField(choices=MATERIAL_CHOICES, verbose_name="Material")
    is_available = models.BooleanField(default=True, verbose_name="Available")
    featured = models.BooleanField(default=False, verbose_name="Featured Product")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    # Main product image
    product_image = models.ImageField(upload_to='products/', verbose_name="Product Image")
    # Optional extra images
    product_image2 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image 2")
    product_image3 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image 3")
    product_image4 = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image 4")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']  # პროდუქტები დალაგდება სახელებით ანბანის მიხედვით

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
