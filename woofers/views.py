from rest_framework import status, views, response, generics
from rest_framework.views import APIView
from .models import User, Veterinary
from .serializers import UserSerializer, LoginSerializer, VeterinarySerializer, ReviewSerializer
from django.contrib.auth import authenticate , login
from django.contrib import auth
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

@method_decorator(ensure_csrf_cookie, name='dispatch') 
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        # Log in the user
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)  # serialize the user data
        return response.Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
    
class LogoutView(views.APIView):
    def post( self, request, format=None):
        try:
            auth.logout(request)
            return response.Response({ 'success' : 'Logged Out'})
        except:
             return response.Response({ 'success' : 'Error while logging out'})

class UpdateUserView(views.APIView):

    def put(self, request, *args, **kwargs):
        # Get the token from the request headers
        token = request.headers.get('Authorization')
        if not token:
            return response.Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        parts = token.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'token':
            return response.Response({"detail": "Invalid token header. No credentials provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # The actual token is the second part of the header
        token = parts[1]
        # Remove the 'Token' prefix

        # Authenticate the user
        user = authenticate(request, token=token)
        if user is None:
            return response.Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        # Proceed with updating the user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     
        
@login_required
def current_user(request):
    user = request.user
    return JsonResponse({
        'email': user.email,
        'username': user.username
    })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return response.Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            auth_user = authenticate(username=user.email, password=request.data.get('password'))
            if auth_user is not None:
                login(request, auth_user)
            else:
                return response.Response({'error': 'Authentication failed.'}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            response_data = {'token': token.key, 'user': UserSerializer(user).data}
            # Log the response data
            return response.Response(
                {'token': token.key, 'user': UserSerializer(user).data}, 
                status=status.HTTP_201_CREATED
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@method_decorator(ensure_csrf_cookie, name='dispatch') 
class GetCSRFToken(views.APIView):
    def get(self, request, format=None):
        return response.Response({ 'success': 'CSRF Cookie set'})
    

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class VeterinaryListCreateView(generics.ListCreateAPIView):
    queryset = Veterinary.objects.all()
    serializer_class = VeterinarySerializer

class VeterinaryDetailView(generics.RetrieveAPIView):
    queryset = Veterinary.objects.all()
    serializer_class = VeterinarySerializer
    
class PostReview(views.APIView):
    def post_review(request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)