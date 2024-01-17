from rest_framework import serializers
from .models import User, Veterinary, Review
from django.contrib.auth import authenticate , get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'date_joined', 'last_login' ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if user is not None:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
                data['user'] = user
                return data
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg)
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'review', 'created_at']
        
class VeterinarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinary
        fields = ['id', 'first_name', 'last_name', 'email', 'location', 'gender', 'created_at', 'reviews']
