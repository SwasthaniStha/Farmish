from django.db import models
from django.utils import timezone

def default_category_id():
    default_category = Category.objects.get_or_create(name='Default')[0]
    return default_category.id

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    farmer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rate (NPR)')
    total_quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to='product_images/', max_length=None)
    Listed_Date = models.DateTimeField(default=timezone.now)
    lifespan = models.IntegerField(default=0, help_text="Lifespan in days")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=default_category_id)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    from django.db import models
from django.utils import timezone

def default_category_id():
    default_category = Category.objects.get_or_create(name='Default')[0]
    return default_category.id

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    farmer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rate (NPR)')
    total_quantity = models.PositiveIntegerField(default=0)
    sold_quantity = models.PositiveIntegerField(default=0)
    product_image = models.ImageField(upload_to='product_images/', max_length=None)
    listed_date = models.DateTimeField(default=timezone.now)
    lifespan = models.IntegerField(default=0, help_text="Lifespan in days")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=default_category_id)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def available_quantity(self):
        return self.total_quantity - self.sold_quantity
    
    def save(self, *args, **kwargs):
        # Calculate and set available_quantity before saving
        self.available_quantity = self.total_quantity - self.sold_quantity
        super().save(*args, **kwargs)


    def __str__(self):
        return self.product_name


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the product first

    def __str__(self):
        return self.product_name
