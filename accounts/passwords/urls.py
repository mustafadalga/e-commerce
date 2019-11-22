# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path
from django.urls import reverse_lazy

urlpatterns = [
    path('password_change/', views.PasswordChangeView.as_view(success_url=reverse_lazy("password:password_change_done")), name='password_change'),
    path('password_change_done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(success_url=reverse_lazy("password:password_reset_done")), name='password_reset'), # Parola sıfırlamak için mail adresi
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'), # Mail adresine sıfırlama link gönderildi sayfası
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("password:password_reset_complete")), name='password_reset_confirm'), # Yeni mail parolası belirleme
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Parola sıfırlama başarıyla tamamlandı sayfası
]