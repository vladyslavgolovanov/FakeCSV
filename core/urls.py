from .views import UserAccountLoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('login/', UserAccountLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')]