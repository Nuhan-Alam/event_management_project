from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, default='profile_images/default.png')
    number = models.CharField(max_length=13)

    def clean(self):
        super().clean()
        errors = []
        if self.number:
            # Custom validation logic
            if not self.number.isdigit():
                errors.append('Number must contain only digits.')
            
            if len(self.number) < 10:
                errors.append('Number must be at least 10 digits long.')
            
            # Check for uniqueness
            if CustomUser.objects.filter(number=self.number).exclude(pk=self.pk).exists():
                errors.append('This number is already in use.')
            
            if errors:
                raise ValidationError(errors)

    def __str__(self):
        return self.username