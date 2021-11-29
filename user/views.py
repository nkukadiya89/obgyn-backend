import json

from django.contrib.auth.hashers import check_password
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from email_util.send_user_email import generate_token, decode_token, send_mail
from .models import User
from .serializers import UserSerializers




# Create your views here.

# REGISTER HOSPITAL/DOCTOR/STAFF
@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        user = User()

        serializer = UserSerializers(user, data=request.data)

        data = {}
        if serializer.is_valid():

            new_user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            data['response'] = "successfully register a new user."
            data['email'] = new_user.email
        else:
            data = serializer.errors
        return Response(data)


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
def get_user(request, type, id=None):
    try:
        user = User.objects.filter(deleted=0)
        if type:
            user = User.objects.filter(user_type=type.upper())

        if id:
            user = user.filter(pk=id)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serilizer = UserSerializers(user, many=True)
        return Response(serilizer.data)


# CHANGE PASSWORD
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    data = request.data
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if check_password(old_password, user.password):
        user.set_password(new_password)
        user.save()
    else:
        return Response("Old Password is incorrect", status=404)
    return Response("Password successfully changed", status=200)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@csrf_exempt
def forget_password(request):
    data = json.loads(request.body.decode('utf-8'))

    email = data.get("email", None)
    if email == None:
        return HttpResponse("No Email Address found", status=404)

    token = generate_token(email, 60)

    user = User.objects.filter(email=email).first()

    if user == None:
        return HttpResponse("Business is not registered with this email", status=404)

    name = user.first_name
    context = {}

    context["name"] = name
    context["token"] = token
    context["email"] = email
    urlObject = request._current_scheme_host + request.path
    context["current_site"] = urlObject
    send_mail("Reset Your Password", "reset-pass.html", context)
    return HttpResponse("Mail has been sent to your registered email", status=200)


@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def reset_password(request, token):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return HttpResponse("Service not available", status=404)

    try:
        payload = decode_token(token)
    except:
        return HttpResponse("Token Expired", status=404)

    if "email" not in payload:
        return HttpResponse("No email found", status=404)

    user = User.objects.filter(email=payload["email"]).first()

    if user == None:
        return HttpResponse("No user found", status=404)

    password = data.get("password", None)

    if password == None:
        return HttpResponse("Reset Password not available", status=404)

    user.set_password(password)
    user.save()

    return HttpResponse("Password successfully changed", status=200)
