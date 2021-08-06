
from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.http.request import MediaType
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """ Creates and saves a superuser with the given email, date ofbirth and password.
        """
        user = self.create_user(
            username=username,
            first_name='',
            last_name='',
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True
    )
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_of_birth = models.DateField(default='1995-03-25')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Customers(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=25)
    time_joined = models.DateTimeField(auto_now_add=True)
    city = models.ForeignKey(to='restaurants.City', on_delete=models.CASCADE,blank=True,null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username