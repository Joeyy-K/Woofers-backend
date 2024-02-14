from rest_framework import serializers, exceptions
from .models import User, Veterinary, Review, Appointment
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'date_joined', 'last_login' ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

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
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['user', 'veterinary', 'review', 'created_at']
        
    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
            return super().create(validated_data)
        else:
            raise exceptions.AuthenticationFailed('User must be authenticated to create a review.')

        
class VeterinarySerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Veterinary
        fields = ['id', 'first_name', 'last_name', 'email', 'location', 'gender', 'created_at', 'reviews']
        
class AppointmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    veterinary = VeterinarySerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'veterinary', 'date', 'time', 'created_at', 'reason_for_visit', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        veterinary_id = self.context['request'].data.get('veterinary')
        veterinary = Veterinary.objects.get(id=veterinary_id)
        if user.is_authenticated:
            validated_data['user'] = user
            validated_data['veterinary'] = veterinary
            return super().create(validated_data)
        else:
            raise exceptions.AuthenticationFailed('User must be authenticated to create an appointment.')


