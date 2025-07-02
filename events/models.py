from django.db import models
from django.core.validators import EmailValidator


class Category(models.Model):
    """
    Category model for event classification
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Event model with all required fields
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='events'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


class Participant(models.Model):
    """
    Participant model with ManyToMany relationship to Event
    """
    name = models.CharField(max_length=150)
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()]
    )
    events = models.ManyToManyField(
        Event,
        related_name='participants',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    