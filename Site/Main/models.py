from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .manager import MyUserManager   
from django.db.models.signals import post_delete
import random
import string
import os

# Custom models
class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_("username"), unique=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_registered = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20)
    slug_identifier = models.SlugField(max_length=200, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = MyUserManager()
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug_identifier:
            self.slug_identifier = slugify(self.username)
        super().save(*args, **kwargs)

class ItemCategory(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    parent_category = models.ForeignKey('self',
                                        on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='subcategories')
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=40, null=True)
    description = models.TextField()
    price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    updated_on = models.DateTimeField(auto_now=True)
    slug_identifier = models.SlugField(unique=True, blank=True, null=True)
    owner_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    ad_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=True, blank=True)
    
    SIZE_CHOICES = (
        ('N', 'New'),
        ('as_new', 'as new'),
        ('U', 'Used'),
    )
    size = models.CharField(max_length=6, choices=SIZE_CHOICES, default='N')
    
    def __str__(self):
        return self.title

    def get_related_images(self):
        return self.images.all() if self.images.exists() else []

    def save(self, *args, **kwargs):
        if not self.slug_identifier:
            self.slug_identifier = slugify(self.title)
        super(Ad, self).save(*args, **kwargs)

class AdImage(models.Model):
    advertisement = models.ForeignKey(Ad,
                                      related_name='images',
                                      on_delete=models.CASCADE
                                      )
    image_file = models.ImageField(upload_to='ad_images/')
    
    def delete(self, *args, **kwargs):
        # Remove the image file from the filesystem
        if self.image_file:
            if os.path.isfile(self.image_file.path):
                os.remove(self.image_file.path)
        super().delete(*args, **kwargs)

def generate_unique_identifier():
    while True:
        unique_token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if not Ad.objects.filter(token=unique_token).exists():
            return unique_token

@receiver(post_delete, sender=Ad)
def remove_ad_image_files(sender, instance, **kwargs):
    for img in instance.images.all():
        img.delete()  #custom delete method of AdImage