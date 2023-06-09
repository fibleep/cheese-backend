from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from .common import ROLES


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_manager(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.role = 2
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.role = 3
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.PositiveIntegerField(unique=False, null=True, blank=True)
    is_active = models.BooleanField(_("Is active User"), default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.PositiveIntegerField(
        _("User role"), choices=ROLES, default=1)
    join_date = models.DateTimeField(
        _("User Join Date"),
        auto_now_add=True)
    last_loggin = models.DateTimeField(
        _("Last loggin Date"),
        auto_now_add=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name, self.pk)
    
    def __str__(self):  
        return str(self.full_name)


