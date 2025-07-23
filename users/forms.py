from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group
# from tasks.forms import StyledFormMixin
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser


from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

def validate_password_rules(password):
    errors = []

    if len(password) < 1:
        errors.append('Password must be at least 1 character long')

    # if not re.search(r'[A-Z]', password1):
    #     errors.append(
    #         'Password must include at least one uppercase letter.')

    # if not re.search(r'[a-z]', password1):
    #     errors.append(
    #         'Password must include at least one lowercase letter.')

    # if not re.search(r'[0-9]', password1):
    #     errors.append('Password must include at least one number.')

    # if not re.search(r'[@#$%^&+=]', password1):
    #     errors.append(
    #         'Password must include at least one special character.')

    if errors:
        raise forms.ValidationError(errors)

class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password', 'confirm_password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password_rules(password)
        return password

    def clean(self):  # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data


class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class AssignRoleForm( forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )
    
class CreateGroupForm(StyledFormMixin,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    def clean_new_password2(self):
        password2 = self.cleaned_data.get("new_password2")
        validate_password_rules(password2)
        return password2
    


class EditProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'number', 'profile_image']