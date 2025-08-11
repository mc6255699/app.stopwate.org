from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # keep record if owner deleted
        null=True,
        blank=True,
        related_name='owned_organizations'
    )
    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    note = models.TextField(blank=True)
    # Phone number with simple validation for digits, +, - and spaces
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,  # keep record if organization deleted
        null=True,
        blank=True,
        related_name='contacts'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # keep record if owner deleted
        null=True,
        blank=True,
        related_name='owned_contacts'
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ContactList(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    contacts = models.ManyToManyField(Contact, blank=True, related_name='contact_lists')
    # Self-referential many-to-many for sublists
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # keep record if owner deleted
        null=True,
        blank=True,
        related_name='owned_contactlists'
    )
    sublists = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='parent_lists'
    )

    def __str__(self):
        return self.name
