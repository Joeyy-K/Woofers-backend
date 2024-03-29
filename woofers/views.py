from django.http import HttpResponse
from rest_framework import status, views, response, generics, permissions
from .models import User, Veterinary, Appointment, City, Country
from .serializers import UserSerializer, LoginSerializer, VeterinarySerializer, ReviewSerializer, AppointmentSerializer, CountrySerializer, CitySerializer
from django.contrib.auth import authenticate , login
from django.contrib import auth
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@method_decorator(ensure_csrf_cookie, name='dispatch') 
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True) # validates the user
        user = serializer.validated_data.get('user')
        login(request, user) # logs in the user
        token, created = Token.objects.get_or_create(user=user) # creates token for user
        user_serializer = UserSerializer(user)  # serialize the user data
        
        res = response.Response({'user': user_serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
        # response that is to be sent to the frontend
        res.set_cookie('userToken', token.key, httponly=False) # token is set in cookie

        return res
    
class LogoutView(views.APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            response = HttpResponse("You're logged out.")
            response.delete_cookie('csrftoken')
            return response
        except:
            return response.Response({ 'success' : 'Error while logging out'})

class UpdateUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return response.Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST) # checks if user with emails already exits
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            auth_user = authenticate(username=user.email, password=request.data.get('password'))
            if auth_user is not None:
                login(request, auth_user) #logs in the user
            else:
                return response.Response({'error': 'Authentication failed.'}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user) # creates token for user
            user_serializer = UserSerializer(user) 
                        
            res = response.Response({'user': user_serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
            # response that will be sent to the frontend
            res.set_cookie('userToken', token.key, httponly=False) # token is set and will be used to authorize the users actions

            return res
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  
    
@method_decorator(ensure_csrf_cookie, name='dispatch') 
class GetCSRFToken(views.APIView):
    def get(self, request, format=None):
        return response.Response({ 'success': 'CSRF Cookie set'})
class VeterinaryListCreateView(generics.ListCreateAPIView):
    queryset = Veterinary.objects.all()
    serializer_class = VeterinarySerializer

class VeterinaryDetailView(generics.RetrieveAPIView):
    queryset = Veterinary.objects.all()
    serializer_class = VeterinarySerializer
    
class PostReview(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AppointmentView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class UserAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user=user)
    
class AppointmentDeleteView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)

class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer