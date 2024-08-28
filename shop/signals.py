from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Product
from PIL import Image
import random

@receiver(post_save, sender=Product)
def resize_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        img = Image.open(image_path)
        img = img.resize((474, 533), Image.Resampling.LANCZOS)
        img.save(image_path)

def generate_numeric_sku():
    return ''.join(str(random.randint(0, 9)) for _ in range(12))

@receiver(pre_save, sender=Product)
def generate_sku(sender, instance, **kwargs):
    if not instance.sku:
        instance.sku = generate_numeric_sku()