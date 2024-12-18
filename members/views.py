from django.shortcuts import render, HttpResponse
from rest_framework import viewsets
from .serializers import UserProfileSerializer, UserDataSerializer
from .models import UserProfile
from django.shortcuts import render
from rest_framework import viewsets, status
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.views.generic import View
from rest_framework.parsers import MultiPartParser

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            confirm_link = f"https://event-hive-backend-django.vercel.app/members/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                "confirm_email.html", {"confirm_link": confirm_link}
            )

            email = EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "Check your mail for confirmation"})
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "<div style='height:100vh;width:100vw;display:flex;align-items:center;justify-content:center'><h2>Your account is activated. Go to <a target='_blank' href='https://event-hive-client-react-102.onrender.com/login'>https://event-hive-client-react-102.onrender.com/login</a> to login</h2></div>"
        )
    else:
        return redirect("register")


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                s_data = UserDataSerializer(user_profile).data

                return Response(
                    {
                        "token": token.key,
                        "user": s_data,
                    }
                )
            else:
                return Response({"error": "Invalid Credential"})
        return Response(serializer.errors)


class UserLogoutView(APIView):

    def get(self, request):
        print(request.user, "line 100")
        print(request.auth, "line 101")
        request.user.auth_token.delete()
        logout(request)
        return Response("Logged out successfully")


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = serializers.UserPasswordChangeSerializer(data=self.request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            confirm_password = serializer.validated_data["confirm_password"]

            if new_password != confirm_password:
                return Response(
                    {"error": "Passwords do not match"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = request.user
            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors)


class AcivatedView(View):
    template_name = "activated.html"
