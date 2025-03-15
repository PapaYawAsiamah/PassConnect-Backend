from django.urls import path
from .views import CheckAuthView, SigninView, SignupView, SignoutView, csrf_token_view, AdminLoginView, EventCreateView, EventUpdateView, EventDeleteView, EventListView, UserRegisteredEventsView, EventRegisterView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('csrf/', csrf_token_view, name='csrf'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('user/events/', UserRegisteredEventsView.as_view(), name='user-registered-events'),
    path('events/<int:pk>/register/', EventRegisterView.as_view(), name='event-register'),
]