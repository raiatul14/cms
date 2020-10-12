from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, address,\
            city, state, country, pincode, password=None, is_admin=False, \
            is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not phone:
            raise ValueError("User must have a phone number")
        if not pincode:
            raise ValueError("User must have a pincode number")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.address = address
        user.city = city
        user.state = state
        user.country = country
        user.pincode = pincode
        user.set_password(password)  # change password to hash
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  first_name, last_name, phone,\
            pincode, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not phone:
            raise ValueError("User must have a phone number")
        if not pincode:
            raise ValueError("User must have a pincode number")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.pincode = pincode
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    USERNAME_FIELD = 'email'

    email = models.CharField(max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=300)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=15)
    phone = models.IntegerField()
    address = models.TextField(max_length=160, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'pincode']
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'