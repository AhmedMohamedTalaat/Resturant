from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt
import datetime
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        name = request.data['name']
        password = request.data['password']
        user = User.objects.filter(name=name).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }
        token = jwt.encode(payload, 'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated!')

        user = User.objects.get(pk=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        respose = Response()
        respose.delete_cookie('jwt')
        return respose
