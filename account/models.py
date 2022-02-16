from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid, random

USERNAME_REGEX = '^[a-zA-Z0-9@.-_]*$'

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        """ Creates and saves an User """
        if not email:
          raise ValidationError('User must have an email address')
        
        if not username:
          username = email.split('@')[0] + str(random.randint(11111, 999999))
        
        user = self.model(
          email=self.normalize_email(email),
          username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password, username=None):
        """ Creates and saves a Staff User """
        if not email:
          raise ValidationError('User must have an email address')
        
        user = self.create_user(
          email=self.normalize_email(email),
          username=username
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        """ Creates and saves a Superuser """
        if not email:
          raise ValidationError('User must have an email address')
        
        user = self.create_user(
          email=self.normalize_email(email),
          username=username
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    username = models.CharField(
      verbose_name='Username', 
      max_length=40, 
      validators=[
        RegexValidator(
          regex=USERNAME_REGEX, 
          message='username must be alphanumeric. Can contain characters like @ . - _',
          code='invalid_username'
        )
      ]
    )
    email = models.EmailField(verbose_name='Email Address', max_length=120, unique=True)
    name = models.CharField(verbose_name='Your Full Name', max_length=50)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    is_admin = models.BooleanField(verbose_name='Admin User', default=False)
    is_staff = models.BooleanField(verbose_name='Staff User', default=False)
    is_superuser = models.BooleanField(verbose_name='Super User', default=False)
    is_active = models.BooleanField(verbose_name='Active User', default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
      return self.email
    
    def __unicode__(self):
      return self.email

    def has_perm(self, perm, obj=None):
      return self.is_admin
    
    def has_module_perms(self, app_label):
      return True