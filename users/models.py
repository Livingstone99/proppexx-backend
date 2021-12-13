from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .utils import (phone_regex, upload_location,)
from django.utils import timezone
from django.db.models import Avg
from users.utils import upload_avatar_path, validate_image
# import rating.models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(
            self, email, first_name,
            password,  **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        now = timezone.now()

        # this was done because self.models keep throwing required field exceptions
        phone_number = ''
        is_staff = False
        last_name = ''
        user = self.model(
            email=email,
            first_name=first_name,
            # last_name=last_name,
            # phone_number=phone_number,
            # is_staff=is_staff,
            is_active=True,
            # is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            ** extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
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
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    USER_TYPE_CHOICES = (
        ('agent', 'agent'),
        ('buyer', 'buyer'),
        ('admin', 'admin'),
        ('developer', 'developer'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES,
                                 blank=True,
                                 null=True,
                                 max_length=30
                                 )
    email = models.EmailField(_('email address'),  unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone_number = models.CharField(
        max_length=11, validators=[phone_regex], default="",
        blank=True,
    )
    about = models.CharField(max_length=150, null=True, blank=True)
    accept_newsletter = models.BooleanField(_('newsletter'), default=False)
    avatar = models.ImageField(upload_to=upload_avatar_path, validators=[validate_image],
                               blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(
        _('last joined'), auto_now_add=False, auto_now=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_email_verified = models.BooleanField(
        _('is email verified'), default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"
        unique_together = ("email", )
        get_latest_by = ['date_joined']

    def __str__(self):
        return str(self.email)

    def get_email(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Agent(models.Model):

    agents = models.OneToOneField(User,
                                  on_delete=models.CASCADE,
                                  primary_key=True, related_name='agent_profile')
    verified = models.BooleanField(default=False)
    rating = models.IntegerField(editable=False, null=True, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "agents"

    def rating(self):
        from rating.models import AgentRating
        agent = AgentRating.objects.filter(agent_user=self.pk)
        try:
            agent[0]
            avg = agent.aggregate(Avg('rate'))
            return f"{avg['rate__avg']}"
        except IndexError:
            return 'no rating yet'
    ratings = property(rating)

    def total_reviewer(self):
        from rating.models import AgentRating
        agent = AgentRating.objects.filter(agent_user=self.pk).count()
        return f'{agent}'
    total_rev = property(total_reviewer)

    def __str__(self):
        return str(self.agents)


class Buyer(models.Model):
    buyers = models.OneToOneField(User,
                                  on_delete=models.CASCADE,
                                  primary_key=True, related_name='buyer_profile')

    class Meta:
        verbose_name_plural = "buyers"

    def __str__(self):
        return str(self.buyers)
