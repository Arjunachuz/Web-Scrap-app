from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=10)
    rating = models.FloatField(max_length=15, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.product.title
