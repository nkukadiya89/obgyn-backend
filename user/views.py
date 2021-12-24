import json

from decouple import config
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from email_util.send_user_email import generate_token, decode_token, send_mail
from utility.search_filter import pagination, camel_to_snake
from .models import User
from .serializers import UserSerializers


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
                user = User.objects.all()
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


def filter_fields(user, filter_fields):
    for fields in filter_fields:
        fld_name = camel_to_snake(fields.split("=")[0])
        fld_value = fields.split("=")[1]
        if fld_name == "first_name":
            user = user.filter(first_name__iexact=fld_value)
        if fld_name == "middle_name":
            user = user.filter(middle_name__iexact=fld_value)
        if fld_name == "last_name":
            user = user.filter(last_name__iexact=fld_value)
        if fld_name == "user_type":
            user = user.filter(user_type__iexact=fld_value)
        if fld_name == "hospital_name":
            user = user.filter(hospital_name__iexact=fld_value)
        if fld_name == "phone":
            user = user.filter(phone=fld_value)
        if fld_name == "state_id":
            user = user.filter(state_id=fld_value)
        if fld_name == "city_id":
            user = user.filter(city_id=fld_value)
        if fld_name == "area_id":
            user = user.filter(area_id=fld_value)
        if fld_name == "pincode":
            user = user.filter(pincode=fld_value)
        if fld_name == "email":
            user = user.filter(email__iexact=fld_value)
        if fld_name == "landline":
            user = user.filter(landline=fld_value)
        if fld_name == "fax_number":
            user = user.filter(fax_number=fld_value)
        if fld_name == "degree":
            user = user.filter(degree__iexact=fld_value)
        if fld_name == "speciality":
            user = user.filter(speciality__iexact=fld_value)
        if fld_name == "aadhar_card":
            user = user.filter(aadhar_card__iexact=fld_value)
        if fld_name == "registration_no":
            user = user.filter(registration_no=fld_value)
        if fld_name == "default_language_id":
            user = user.filter(default_language_id=fld_value)
        if fld_name == "designation":
            user = user.filter(designation__iexact=fld_value)
        if fld_name == "designation":
            user = user.filter(registration_no=fld_value)
    return user


def search(user, search):
    if search:
        user = user.filter(
            Q(first_name__icontains=search) |
            Q(middle_name__icontains=search) |
            Q(user_type__icontains=search) |
            Q(hospital_name__icontains=search) |
            Q(state__state_name__icontains=search) |
            Q(city__city_name__icontains=search) |
            Q(email__icontains=search) |
            Q(landline__icontains=search) |
            Q(fax_number__icontains=search) |
            Q(degree__icontains=search) |
            Q(speciality__icontains=search) |
            Q(aadhar_card__icontains=search) |
            Q(registration_no__icontains=search) |
            Q(default_language__language__icontains=search) |
            Q(designation__icontains=search) |
            Q(username__icontains=search)
        )
    return user


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_user(request, type, id=None):
    query_string = request.query_params

    if "orderBy" not in query_string:
        orderby = "id"
    else:
        orderby = camel_to_snake(str(query_string["orderBy"]))

    if "sortBy" not in query_string:
        sortby = ""
    else:
        sortby = str(query_string["sortBy"])
        if sortby.lower() == "desc":
            sortby = "-"
        else:
            sortby = ""

    data = {}
    try:
        user = User.objects.filter(deleted=0)
        if type:
            user = User.objects.filter(user_type=type.upper())
        if id:
            user = user.filter(pk=id)

        if "filter" in query_string:
            filter = list(query_string["filter"].split(","))
            if filter:
                user = filter_fields(user, filter)
        if "search" in query_string:
            user = search(user, query_string["search"])
        if orderby:
            if sortby:
                orderby = sortby + orderby

            print(orderby)
            user = user.order_by(orderby)
        if "page" in query_string:
            if "pageRecord" in query_string:
                pageRecord = query_string["pageRecord"]
            else:
                pageRecord = config('PAGE_LIMIT')

            user, data["warning"], data["total_page"] = pagination(user, query_string["page"], pageRecord)

    except User.DoesNotExist:
        data["success"] = False
        data["msg"] = "User Does not exist"
        data["data"] = []
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        data["success"] = True
        data["msg"] = "OK"
        serializer = UserSerializers(user, many=True)
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)


# CHANGE PASSWORD
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def change_password(request):
    data = {}
    user = request.user

    data = request.data
    old_password = data.get('old_password')
    new_password = data.get('new_password')

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
def reset_password(request, token):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return HttpResponse("Service not available", status=401)

    try:
        payload = decode_token(token)
    except:
        return HttpResponse("Token Expired", status=401)

    if "email" not in payload:
        return HttpResponse("No email found", status=401)

    user = User.objects.filter(email=payload["email"]).first()

    if user == None:
        return HttpResponse("No user found", status=401)

    password = data.get("password", None)

    if password == None:
        return HttpResponse("Reset Password not available", status=401)

    user.set_password(password)
    user.save()

    return HttpResponse("Password successfully changed", status=200)


@csrf_exempt
@authentication_classes(JWTAuthentication)
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(('POST',))
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

    if request.method == "POST":
        result = user.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)
