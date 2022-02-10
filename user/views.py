import json

from django.contrib.auth.hashers import check_password
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from email_util.send_user_email import generate_token, decode_token, send_mail
from utility.search_filter import user_filtering_query
from .models import User
from .serializers import UserSerializers, DynamicFieldModelSerializer
from django.utils.timezone import now


# Create your views here.

# REGISTER HOSPITAL/DOCTOR/STAFF
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == 'POST':
        user = User()

        serializer = UserSerializers(user, data=request.data)

        data = {}
        if serializer.is_valid():
            new_user = serializer.save()
            user.set_password(request.data["password"])
            user.uid = str(now()).replace("-", "").replace(":", "").replace(" ", "").replace(".", "").split("+")[0][:16]
            user.save()
            data["success"] = True
            data["msg"] = "OK"
            data['response'] = "Successfully register a new user."
            data['email'] = new_user.email
        else:
            data["success"] = False
            data["msg"] = "User Registration Failed."
            data["errors"] = serializer.errors
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if user.user_type == "HOSPITAL":
            name = user.hospital_name
        else:
            name = user.first_name

        email = user.email
        token = generate_token(email, 2880)
        context = {}
        context["name"] = name
        context["token"] = token
        context["email"] = email

        urlObject = request._current_scheme_host + request.path
        context["current_site"] = urlObject
        send_mail("Registration Successful", "register-success.html", context)
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def update_user(request, id):
    data = {}

    if request.method == "POST":
        try:
            if id:
                user = User.objects.get(pk=id)
            else:
                user = User.objects.filter(deleted=0)
        except User.DoesNotExist:
            data["success"] = False
            data["msg"] = "User does not exist"
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "POST":
            serializer = UserSerializers(user, request.data, partial=True)
            if serializer.is_valid():
                user = serializer.save()

                if "password" in request.data:
                    user.set_password(request.data["password"])
                    user.save()

                data["success"] = "Update successful"
                data["success"] = True
                data["msg"] = "OK"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data["success"] = False
                data["msg"] = "Update user fail."
                data["errors"] = serializer.errors
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user(request, type, id=None):
    query_string = request.query_params

    data = {}
    try:
        user = User.objects.filter(deleted=0)
        if type:
            user = User.objects.filter(user_type__iexact=type.upper(), deleted=0)
        if id:
            user = user.filter(pk=id, deleted=0)

        data["total_record"] = len(user)
        user, data = user_filtering_query(user, query_string, "id", "USER")

    except User.DoesNotExist:
        data["success"] = False
        data["msg"] = "User Does not exist"
        data["data"] = []
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        data["success"] = True
        data["msg"] = "OK"

        serializer = UserSerializers(user, many=True)
        if "fields" in query_string:
            if query_string["fields"]:
                serializer = DynamicFieldModelSerializer(user, many=True, fields=query_string["fields"])

        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user_field_wise(request, type, id=None):
    query_string = request.query_params

    data = {}
    try:
        user = User.objects.filter(deleted=0)
        if type:
            user = User.objects.filter(user_type__iexact=type.upper(), deleted=0)
        if id:
            user = user.filter(pk=id, deleted=0)

        data["total_record"] = len(user)
        user, data = user_filtering_query(user, query_string, "id", "USER")

    except User.DoesNotExist:
        data["success"] = False
        data["msg"] = "User Does not exist"
        data["data"] = []
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        data["success"] = True
        data["msg"] = "OK"
        user = user
        serializer = DynamicFieldModelSerializer(user, many=True, fields=query_string["fields"])
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# CHANGE PASSWORD
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def change_password(request):
    data = {}
    user = request.user

    req_data = request.data
    old_password = req_data.get('old_password')
    new_password = req_data.get('new_password')

    if check_password(old_password, user.password):
        user.set_password(new_password)
        user.save()
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = "Password successfully changed."
    else:
        data["success"] = False
        data["msg"] = "Old Password is incorrect."
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    return Response(data=data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@csrf_exempt
@api_view(('POST',))
def forget_password(request):
    data = json.loads(request.body.decode('utf-8'))
    resp_data = {}
    email = data.get("email", None)
    if email == None:
        resp_data["success"] = False
        resp_data["msg"] = "No Email Address found"

        return Response(data=resp_data, status=status.HTTP_401_UNAUTHORIZED)

    token = generate_token(email, 60)

    user = User.objects.filter(email=email).first()

    if user == None:
        resp_data["success"] = False
        resp_data["msg"] = "Business is not registered with this email"
        return Response(data=resp_data, status=status.HTTP_401_UNAUTHORIZED)

    name = user.first_name

    context = {}
    context["name"] = name
    context["token"] = token
    context["email"] = email
    urlObject = request._current_scheme_host + request.path
    context["current_site"] = urlObject
    send_mail("Reset Your Password", "reset-pass.html", context)

    resp_data["success"] = True
    resp_data["msg"] = "Mail has been sent to your registered email"
    return Response(data=resp_data, status=status.HTTP_200_OK)


@csrf_exempt
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
@api_view(('POST',))
def reset_password(request, token):
    data = {}
    try:
        res_data = json.loads(request.body.decode('utf-8'))
    except:
        data["success"] = False
        data["msg"] = "Service Not available"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = decode_token(token)
    except:
        data["success"] = False
        data["msg"] = "Token Expired"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if "email" not in payload:
        data["success"] = False
        data["msg"] = "Inavalid Token"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(email=payload["email"]).first()

    if user == None:
        data["success"] = False
        data["msg"] = "Email not registered"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    password = res_data.get("password", None)

    if password == None:
        data["success"] = False
        data["msg"] = "Provide valid Password"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    user.set_password(password)
    user.save()

    data["success"] = True
    data["msg"] = "Password sucessfully changed"
    return Response(data=data, status=status.HTTP_200_OK)


@csrf_exempt
@authentication_classes(JWTAuthentication)
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(('DELETE',))
def delete_user(request):
    body = json.loads(request.body.decode('utf-8'))
    data = {}
    if "id" not in body:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.filter(id__in=body["id"])
    except User.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = user.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


@csrf_exempt
@authentication_classes(JWTAuthentication)
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(('POST',))
def verify_user(request, token):
    data = {}
    try:
        payload = decode_token(token)
    except:
        data["success"] = False
        data["msg"] = "Provided Token is Expired"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if "email" not in payload:
        data["success"] = False
        data["msg"] = "This email is not registered"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(email=payload["email"]).first()

    if user == None:
        data["success"] = False
        data["msg"] = "Record Not Found"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    user.verified = True
    user.save()

    data["success"] = True
    data["msg"] = "Account verified"
    return Response(data=data, status=status.HTTP_200_OK)


@csrf_exempt
@authentication_classes(JWTAuthentication)
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(('POST',))
def send_verify_link(request):
    data = {}
    try:
        req_data = json.loads(request.body.decode('utf-8'))
    except:
        data["success"] = False
        data["msg"] = "Service not available"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    email = req_data.get("email", None)
    if email == None:
        data["success"] = False
        data["msg"] = "Email Address is not registered"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.filter(email=email).first()

    if user == None:
        data["success"] = False
        data["msg"] = "Record Not Found"
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    verify_user = User.objects.filter(id=user.id).first()

    if verify_user.verified:
        data["success"] = False
        data["msg"] = "Account is already verified"
        return Response(data=data, status=status.HTTP_200_OK)

    token = generate_token(email, 2880)

    if user.user_type == "HOSPITAL":
        name = user.hospital_name
    else:
        name = user.first_name
    context = {}

    context["name"] = name
    context["token"] = token
    context["email"] = email
    urlObject = request._current_scheme_host + request.path
    context["current_site"] = urlObject
    send_mail("Verify Your Account", "verify_account.html", context)
    data["success"] = True
    data["msg"] = "Email has been send"
    return Response(data=data, status=status.HTTP_200_OK)
