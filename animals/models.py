
from django.db import models
from django.contrib.auth.models import User


class Species(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Breed(models.Model):
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name='breeds'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('species', 'name')
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.species.name})'


class Location(models.Model):
    name = models.CharField(max_length=150)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Pending', 'Pending'),
        ('Adopted', 'Adopted'),
    ]

    name = models.CharField(max_length=100)
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name='animals'
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='animals'
    )
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    description = models.TextField(blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='animals'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )

    # Animal photo upload
    image = models.ImageField(
        upload_to='animals/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='adoption_requests'
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='adoption_requests'
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.applicant.username} - {self.animal.name}'
