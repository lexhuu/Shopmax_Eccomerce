from django.urls import path
from users import views
from django.contrib.auth import views as auth_views
from users.forms import NewUserPasswordChangeForm, NewUserPasswordResetEmailForm, NewUserPasswordResetForm

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.profile_user, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html', form_class=NewUserPasswordChangeForm, success_url = '/'), name='password_change'), 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=NewUserPasswordResetEmailForm), name='password_reset'), 
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),      
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=NewUserPasswordResetForm), name='password_reset_confirm'), 
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),      
]