from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import requests


class UserCustomerManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required to create user")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required to create user")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserCustomerManager()


class Category(models.Model):
    name=models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Product(models.Model):
    WATCH_CHOICES = (
        ("Men", "Men"),
        ("Women", "Women")
    )
    name=models.CharField(max_length=256, null=False, default="No Name ")
    type=models.CharField(choices=WATCH_CHOICES, max_length=256)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.CharField(max_length=256)
    date_added=models.DateTimeField(auto_now_add=True)
    description=models.TextField(null=True)
    image=models.ImageField(upload_to='images/')


class Cart(models.Model):
    product=models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    quantity=models.IntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    date_added=models.DateTimeField(auto_now_add=True)

PAYMENT_CHOICES = (
    ("MTN Rwanda", "MTN Mobile Money"),
    ("Airtel Rwanda", "Airtel Money " )
    )


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=256)
    district = models.CharField(max_length=256,)
    sector = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)
    amount_payed=models.CharField(max_length=256)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=256)


class Message(models.Model):
    body=models.TextField()
    sent_by=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering=('created_at',)

    def __str__(self) -> str:
        return f"{self.created_at}"
    
class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = (
        (WAITING, 'waiting'),
        (ACTIVE, 'active'),
        (CLOSED, 'closed')
    )
    uuid=models.CharField(max_length=255, primary_key=True)
    client=models.CharField(max_length=255)
    agent=models.ForeignKey(User, related_name="room", blank=True, null=True, on_delete=models.SET_NULL)
    messages=models.ManyToManyField(Message, blank=True)
    url=models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=("created_at", )

    def __str__(self) -> str:
        return f"{self.client}"
