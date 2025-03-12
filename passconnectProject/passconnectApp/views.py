from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSignupSerializer, UserSigninSerializer
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
        return Response({"message": "Signin successful"}, status=status.HTTP_200_OK)
    
    
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "User is authenticated"}, status=status.HTTP_200_OK)