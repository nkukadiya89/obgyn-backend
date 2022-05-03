from operator import mod
from re import T
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager  ## A new class is imported. ##
from django.db import models
from django.db.models.query import Q
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from city.models import CityModel
from district.models import DistrictModel
from language.models import LanguageModel
from state.models import StateModel
from taluka.models import TalukaModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    TYPE_CHOICE = (
        ("HOSPITAL", "HOSPITAL"),
        ("STAFF", "STAFF"),
        ("DOCTOR", "DOCTOR"),
        ("PATIENT", "PATIENT")
    )

    first_name = models.CharField(max_length=150, default="")
    last_name = models.CharField(max_length=150, default="")
    user_type = models.CharField(max_length=9, choices=TYPE_CHOICE)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=25, null=True)

    # FIELDS FOR HOSPITAL
    hospital_name = models.CharField(max_length=250, null=True)
    state = models.ForeignKey(StateModel, on_delete=models.DO_NOTHING, null=True, related_name="user")
    taluka = models.ForeignKey(TalukaModel, on_delete=models.DO_NOTHING, null=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING, null=True)
    area = models.CharField(max_length=250, null=True)
    pincode = models.CharField(max_length=20, null=True)
    landmark = models.CharField(max_length=250, null=True)
    default_language = models.ForeignKey(LanguageModel, on_delete=models.SET_DEFAULT, default=1)

    # FIELDS FOR DOCTOR
    hospital = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    middle_name = models.CharField(max_length=150, null=True)
    landline = models.CharField(max_length=15, null=True)
    fax_number = models.CharField(max_length=15, null=True)
    degree = models.CharField(max_length=250, null=True)
    speciality = models.CharField(max_length=500, null=True)
    aadhar_card = models.CharField(max_length=15, null=True)
    registration_no = models.CharField(max_length=25, null=True)
    user_code = models.CharField(max_length=10, default="")
    verified = models.BooleanField(default=False)

    # FIELDS FOR STAFF
    designation = models.CharField(max_length=25, null=True)
    uid = models.CharField(max_length=100, default="")
    

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'


def user_post_save(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        seq_no = 0
        last_user = User.objects.filter(user_type=instance.user_type).filter(~Q(pk=instance.id)).last()

        if last_user:
            seq_no = int(last_user.user_code[-4:])
            seq_no += 1

        instance.user_code = instance.user_type[0] + '{:05}'.format(seq_no)
        instance.save()


post_save.connect(user_post_save, sender=User)
