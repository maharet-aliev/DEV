from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        username = username
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)

# class UserManager(BaseUserManager):
#     use_in_migrations = True
#     def _create_user(self, user_type, email, username, full_name, password, **extra_fields):
#         """
#         Create and save a user with the given username, email,
#         full_name, and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')
#         if not username:
#             raise ValueError('The given username must be set')
#         if not full_name:
#             raise ValueError('The given full name must be set')
#         email = self.normalize_email(email)
#         username = self.model.normalize_username(username)
#
#         user = self.model(user_type=user_type,
#             email=email, username=username, full_name=full_name,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#     def create_user(self, user_type, email, username, full_name, password, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(user_type,
#             email, username, full_name, password, **extra_fields
#         )
#     def create_superuser(self, user_type, email, username, full_name, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self._create_user(user_type,
#             email, username, full_name, password, **extra_fields
#         )

class User(AbstractBaseUser, PermissionsMixin):
    user_types = [
        ('IS_EMPLOYEE_USER', 'Сотрудник'),
        ('IS_CUSTOMER_USER', 'Представитель клиента')

    ]
    user_type = models.CharField(
        verbose_name='Тип пользователя',
        choices=user_types, max_length=50,
        default='unknown', null=True
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(verbose_name = 'Логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(verbose_name='Ф.И.О.', max_length=255)
    mobile = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
    def get_short_name(self):
        return self.email
    def get_full_name(self):
        return self.full_name
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)