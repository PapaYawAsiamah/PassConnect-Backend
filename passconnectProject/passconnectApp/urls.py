from django.urls import path
from .views import CheckAuthView, SigninView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
]