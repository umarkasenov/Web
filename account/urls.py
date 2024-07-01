from .views import RegisterView, ConfirmView
from django.urls import path


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm/', ConfirmView.as_view(), name='confirm')
]
