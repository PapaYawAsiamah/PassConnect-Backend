from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']  # Adjust fields as needed

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        # Send verification email
        send_email_confirmation(self.context['request'], user)
        return user
    
class UserSigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.emailaddress_set.filter(verified=True).exists():
                return user
            raise serializers.ValidationError("Email not verified.")
        raise serializers.ValidationError("Invalid credentials.")