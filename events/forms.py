from django import forms
from events.models import Category,Event



# Styles



class StyledFormMixin:
    """ Mixing to apply style to form field"""
    default_classes= "mb-2 border-2 border-gray-300 w-full rounded-lg shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 p-3 transition"
    date_styles = "border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
    label_styles = "block text-gray-700 font-medium mb-2"

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("Inside Date")
                field.widget.attrs.update({
                    "class": f"{self.date_styles} p-2 ",
                })
            elif isinstance(field.widget, forms.TimeInput):
                # NOT WORKING PROPERLY
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500",
                     'type': 'time',
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })


# Django Model Form
class EventModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category','event_image']
        widgets = {
            'name': forms.TextInput,
            'description':forms.Textarea,
            'date': forms.SelectDateWidget,
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'location': forms.TextInput,
            'category': forms.Select
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


class CateModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'name': forms.TextInput,
            'description':forms.Textarea
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


# class ParticipantModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name','email','events']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': default_styles + "p-3" ,
#                 'placeholder':"Event Name"
#             }),
#              'email': forms.EmailInput(attrs={   
#         'class': default_styles + " p-3",  
#         'placeholder': "Email",
#     }),
#             'events': forms.CheckboxSelectMultiple(attrs={
#                 'class': "space-y-2",  # Added spacing between checkboxes for better readability
#             }),
#         }
#         labels = {
#             'name': 'Participant Name',
#             'email': 'Email Address', 
#             'events': 'Events', 
#         }
    