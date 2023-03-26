from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# choices
USER_ROLES = (
    ('Admin', 'Admin'),
    ('Employee', 'Employee'),
)


class UserCustomManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_number, password, **extra_fields):
        if not user_number:
            raise ValueError('The given employee number must be set')
        user = self.model(user_number=user_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_number, password, **extra_fields)

    def create_superuser(self, user_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_number, password, **extra_fields)


class User(AbstractUser):
    user_number = models.IntegerField(unique=True,  validators=[
            MaxValueValidator(9999),
            MinValueValidator(1000)
        ])
    username = None
    role = models.CharField(max_length=10, choices=USER_ROLES)
    email = models.EmailField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)

    USERNAME_FIELD = 'user_number'
    REQUIRED_FIELDS = []

    objects = UserCustomManager()

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'users'

    def __str__(self):
        return "{}".format(self.user_number)
