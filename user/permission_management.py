from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from user.models import User
from .serializers import GroupSerializers


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def create_new_group(request):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        Group.objects.create(name=request.data.get('name'))
        data["success"] = True
        data["msg"] = "OK"
        data['response'] = "Successfully created new group."
    except IntegrityError as e:
        data["success"] = False
        data['msg'] = "Group creation failed."
        data["response"] = str(e.__cause__).split("\"")[0]

    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def list_group(request,id=None):
    data={}
    try:
        if id:
            group=Group.objects.get(pk=id, deleted=0)
        else:
            group = Group.objects.all()
        
        data["total_record"] = len(group)
    except Group.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializers = GroupSerializers(group, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializers.data
        return Response(data=data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def assign_user_group(request):
    data = {}
    user_ids = request.data.get('user_id')
    user_list = User.objects.filter(pk__in=user_ids)

    group_id = request.data.get('group_id')

    group = Group.objects.get(pk=group_id)

    if group == None:
        data["success"] = False
        data["msg"] = "Group not found."
        data['response'] = "No changes made."
    for user in user_list:
        group.user_set.add(user)

    data["success"] = True
    data["msg"] = "User assigned to group."
    data['response'] = "Update successful."
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def list_permission(request):
    data = {}
    content_type_list = ContentType.objects.filter(id__gt=5).values('id', 'app_label')

    content_type_list = list(content_type_list)

    for content_type in content_type_list:
        permission_list = Permission.objects.filter(content_type_id=content_type["id"])
        for permission in permission_list:
            content_type[permission.codename] = permission.name

    data["total_record"] = len(content_type_list)
    data["success"] = True
    data["msg"] = "OK"
    data["data"] = content_type_list
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def assign_permission_group(request):
    data = {}

    group_id = request.data.get('group_id')
    codename_list = list(request.data.get('codename'))

    group = Group.objects.get(pk=group_id)
    for codename in codename_list:
        code_id = Permission.objects.filter(codename=codename).values('id')[0].get('id')
        group.permissions.add(code_id)


    group_permission = Permission.objects.filter(group=group)
    permission_list = {}
    for permission in group_permission:
        if permission.content_type.app_label in permission_list:
            permission_name = permission_list[permission.content_type.app_label]
            permission_list[permission.content_type.app_label] = ",".join([permission_name,permission.name.split(" ")[1]])
        else:
            permission_list[permission.content_type.app_label] = permission.name.split(" ")[1]

    data["success"] = True
    data["msg"] = "Permission assigned to group."
    data['response'] = permission_list
    return Response(data=data, status=status.HTTP_200_OK)


from user.models import AuthPermissionModel, ContentTypeModel

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_group_permission(request, user_id):
    data = {}
    user = User.objects.get(pk=user_id)
    group_permission = AuthPermissionModel.objects.filter(authgrouppermissionsmodel__group__usergroupsmodel__user_id=user.id)

    permission_list = {}
   
    for permission in group_permission:
        if permission.content_type.app_label in permission_list:
            permission_name = permission_list[permission.content_type.app_label]
            permission_list[permission.content_type.app_label] = ",".join([permission_name,permission.name.split(" ")[1]])
        else:
            permission_list[permission.content_type.app_label] = permission.name.split(" ")[1]
   

    data["total_record"] = len(permission_list)
    data["success"] = True
    data["msg"] = "OK"
    data["data"] = permission_list
    return Response(data=data, status=status.HTTP_200_OK)