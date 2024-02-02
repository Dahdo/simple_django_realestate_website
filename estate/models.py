from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    state = models.CharField(max_length=30, blank=False, null=False)
    city = models.CharField(max_length=30, blank=False, null=False)
    district = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    house_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.state} - {self.city} - {self.district} - {self.postal_code} - {self.street}"


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=True)

    # provide unique relate_names for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_permissions')

    def __str__(self):
        return f"user: {self.first_name} {self.last_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f"profile: {self.user.first_name} {self.user.last_name}"

    @property
    def profile_pic_url(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url

    # Signal to create UserProfile instance when a new CustomUser is created
    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class Property(models.Model):
    PROPERTY_CATEGORIES = [
        ('house', 'House'),
        ('land', 'Land'),
        ('apartment', 'Apartment'),
        ('commercial', 'Commercial'),
    ]
    PROPERTY_STATUS = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent')
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, blank=False, null=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False)
    category = models.CharField(max_length=20, choices=PROPERTY_CATEGORIES, default='house')
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='for_sale')
    image_1 = models.ImageField(upload_to='property_images/', null=True, blank=False)
    image_2 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)  # The property owner

    def __str__(self):
        return f"profile: {self.title}"


class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    orderItem = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    order_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.order_id}"
