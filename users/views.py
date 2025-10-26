from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm,LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from events.forms import StyledFormMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from users.forms import CustomPasswordResetConfirmForm,CustomPasswordResetForm,CustomPasswordChangeForm,EditProfileForm
from django.views.generic import TemplateView,UpdateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')

        else:
            print("Form is not valid")
    return render(request, 'registration/register.html', {"form": form})

# No:1 Conversion to class based view
class SignUpView(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.is_active = False
        user.save()
        messages.success(self.request, 'A Confirmation mail sent. Please check your email')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is not valid")
        return super().form_invalid(form)

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

# @login_required
# def sign_out(request):
#     if request.method == 'POST':
#         logout(request)
#         return redirect('sign-in')
    
@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')
    


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):

    # Debug
    print(f"Current user: {request.user}")
    print(f"User groups: {list(request.user.groups.values_list('name', flat=True))}")
    print(f"Is admin check: {is_admin(request.user)}")

    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/user_list.html', {"users": users})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

# No:5 Conversion to class based view
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
class GroupListView(UserPassesTestMixin, ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    login_url = 'no-permission'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    

@login_required 
def my_list(request):
    user_events = request.user.registered_events.all()
    return render(request, 'participant/my_list.html', {'event_list': user_events,'current_user': request.user,})
# No:4 Conversion to class based view
class MyListView(LoginRequiredMixin, TemplateView):
    template_name = 'participant/my_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_events = self.request.user.registered_events.all()
        context['event_list'] = user_events
        context['current_user'] = self.request.user
        return context

# No:2 Conversion to class based view
from django.contrib.auth.views import LoginView
class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm  

from django.contrib.auth.views import PasswordChangeDoneView
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'events/success.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.success(self.request, 'Your password has been changed successfully!')
        context['context'] = 'Your password has been changed successfully!'
        return context  

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form errors:", form.errors)
        messages.error(self.request, 'Error resetting your password.')
        return super().form_invalid(form)
    

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['number'] = user.number
        if user.profile_image:
            context['profile_image_url'] = user.profile_image.url
        else:
            context['profile_image_url'] = 'https://res.cloudinary.com/dbgsrmvgi/image/upload/v1761485514/default_k1ou2x.png'

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')