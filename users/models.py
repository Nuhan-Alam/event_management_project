from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):

    profile_image = CloudinaryField('image', blank=True, null=True, default='https://res.cloudinary.com/dbgsrmvgi/image/upload/v1761485514/default_k1ou2x.png')
    
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