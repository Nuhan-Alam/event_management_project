from django import forms
from events.models import Category,Event,Participant

# Styles
default_styles= "border-2 border-gray-300 w-full rounded-lg shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 p-3 transition"
date_styles = "border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
label_styles = "block text-gray-700 font-medium mb-2"

# Django Model Form
class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': default_styles + "p-3" ,
                'placeholder':"Event Name"
            }),
            'description':forms.Textarea(attrs={
                'class': default_styles + "p-3 resize-vertical" ,
                'placeholder': "Event Description",
                'rows': 5,
            }),
            'date': forms.SelectDateWidget(attrs={
                'class': date_styles + "p-2",
            }),
            'time': forms.TimeInput(attrs={
                'class': default_styles + "p-2",
                'type': 'time',
            }),
            'location': forms.TextInput(attrs={
                'class': default_styles + "p-3" ,
                'placeholder':"Event Location"
            }),
            'category': forms.Select(attrs={
                'class': "space-y-2",  # Added spacing between checkboxes for better readability
            }),
        }
        labels = {
            'name': 'Event Name',
            'description': 'Event Description', 
            'date': 'Event Date',
            'time': 'Event Time',
            'location': 'Event Location',
            'category': 'Event Categories',
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Apply label styling to all fields
    #     for field_name, field in self.fields.items():
    #         field.label_classes = label_styles


class CateModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': default_styles + "p-3" ,
                'placeholder':"Event Name"
            }),
            'description':forms.Textarea(attrs={
                'class': default_styles + "p-3 resize-vertical" ,
                'placeholder': "Event Description",
                'rows': 5,
            }),
        }
        labels = {
            'name': 'Category Name',
            'description': 'Category Description', 
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Apply label styling to all fields
    #     for field_name, field in self.fields.items():
    #         field.label_classes = label_styles


class ParticipantModelForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email','events']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': default_styles + "p-3" ,
                'placeholder':"Event Name"
            }),
             'email': forms.EmailInput(attrs={   
        'class': default_styles + " p-3",  
        'placeholder': "Email",
    }),
            'events': forms.CheckboxSelectMultiple(attrs={
                'class': "space-y-2",  # Added spacing between checkboxes for better readability
            }),
        }
        labels = {
            'name': 'Participant Name',
            'email': 'Email Address', 
            'events': 'Events', 
        }
    