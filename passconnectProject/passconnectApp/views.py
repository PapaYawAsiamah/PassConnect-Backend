from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSignupSerializer, UserSigninSerializer, EventSerializer
from .models import Event
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import logging

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Sign Up Successful,please verify email"},
            status=status.HTTP_201_CREATED
        )

class SigninView(APIView):
    def post(self, request):
        serializer = UserSigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)  # Log the user in
        
        # Get the session ID
        session_id = request.session.session_key
        
        # If no session key exists, force creation of one
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
            
        return Response({
            "message": "Signin successful",
            "session_id": session_id,
            "user": {
                "username": user.username,
                "email": user.email,
                 "is_staff": user.is_staff  
            }
        }, status=status.HTTP_200_OK)

class AdminLoginView(APIView):
    def post(self, request):
        serializer = UserSigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        if user.is_staff:
            login(request, user)  # Log the user in
            
            # Get the session ID
            session_id = request.session.session_key
            
            # If no session key exists, force creation of one
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
                
            return Response({
                "message": "Admin login successful",
                "session_id": session_id,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "is_staff": user.is_staff  
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Admin login failed. User is not a staff member."
            }, status=status.HTTP_403_FORBIDDEN)

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session_id = request.session.session_key
        return Response({
           
            "session_id": session_id,
            "is_authenticated": True
        }, status=status.HTTP_200_OK)

class SignoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({
            "message": "Signout successful"
        }, status=status.HTTP_200_OK)

class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(created_by=self.request.user)

class EventUpdateView(generics.UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

class EventDeleteView(generics.DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logging.info(f"User: {user}, Authenticated: {user.is_authenticated}")
        return Event.objects.filter(created_by=user)

class UserRegisteredEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.registered_events.all()

class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if event.participants.count() >= event.max_participants:
            return Response({"detail": "Event is full."}, status=status.HTTP_400_BAD_REQUEST)
        
        event.participants.add(request.user)
        return Response({"message": "Successfully registered for the event."}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def csrf(request):
#     return Response({'csrfToken': get_token(request)})


def csrf_token_view(request):
    return JsonResponse({"csrftoken": get_token(request)})