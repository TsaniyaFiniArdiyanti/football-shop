import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    CATEGORY_CHOICES = [
        ('jerseys', 'Jerseys'),
        ('footwear', 'Footwear'),
        ('training', 'Training Gear'),
        ('accessories', 'Accessories'),
        ('equipment', 'Equipment'),
        ('fan_collection', 'Fan Collection'),
        ('kids', 'Kids Collection'),
        ('goalkeeper', 'Goalkeeper Gear'),
        ('retro', 'Retro & Vintage'),
        ('custom', 'Customization'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='custom')
    is_featured = models.BooleanField(default=False)