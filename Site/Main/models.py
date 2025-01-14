import os
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(_("username"), unique=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=20)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

class Category(models.Model):
    category_name = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    def __str__(self):
        return self.category_name

class City(models.Model):
    city_name = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.city_name

class Advertising(models.Model):
    title = models.CharField(max_length=40, null=True)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Advertising, self).save(*args, **kwargs)

class AdvertisingImage(models.Model):
    advertising = models.ForeignKey(Advertising, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads_images/')

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class Note(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Content: {self.content} by {self.sender}"

@receiver(post_delete, sender=Advertising)
def delete_advertising_images(sender, instance, **kwargs):
    for image in instance.images.all():
        image.delete()  # Call the custom delete method of AdvertisingImage