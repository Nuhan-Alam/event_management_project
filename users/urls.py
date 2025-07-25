from django.urls import path
# from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group, group_list
from users.views import (
    sign_in,CustomLoginView,
    sign_up,
    sign_out,
    admin_dashboard,
    assign_role,
    create_group,
    group_list,
    activate_user,
    my_list,
    ProfileView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    ChangePassword,
    CustomPasswordChangeDoneView,
    EditProfileView,
    SignUpView,
    MyListView,
    GroupListView
)
from django.contrib.auth.views import LogoutView # No:5 Conversion to class based view
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/', sign_out, name='logout'),
    path('sign-out/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),
    path('my_list/', MyListView.as_view(), name='my-list'),


    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]