import json

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from utility.search_filter import filtering_query
from .models import AdviceModel, AdviceGroupModel, AdviceGroupAdviceModel
from .serializers import AdviceSerializers, AdviceGroupSerializers
from .utils_view import insert_advice_group
from django.db.models import Q
from utility.decorator import validate_permission, validate_permission_id


class AdviceAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["advice_name"]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            advice = AdviceModel.objects.filter(pk=id).first()
        except AdviceModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = AdviceSerializers(advice, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("advice", "delete")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        advice = AdviceModel.objects.filter(advice_id__in=del_id["id"])
    except AdviceModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = advice.delete()

        AdviceGroupAdviceModel.objects.filter(advicemodel_id__in=del_id["id"]).delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("advice", "add")
def create(request):
    data = {}
    if request.method == "POST":
        advice = AdviceModel()
        serializer = AdviceSerializers(advice, data=request.data)

        if serializer.is_valid():
            serializer.save()
            if "advice_group_name" in request.data:
                insert_advice_group(request, serializer.data["advice_id"])

            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("advice", "change")
def patch(request, id):
    data = {}
    try:
        if id:
            advice = AdviceModel.objects.get(pk=id)
        else:
            advice = AdviceModel.objects.filter(deleted=0)
    except AdviceModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = AdviceSerializers(advice, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("advice", "view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            advice = AdviceModel.objects.filter(pk=id, deleted=0)
        else:
            advice = AdviceModel.objects.filter(
                Q(deleted=0, created_by=1)
                | Q(created_by=request.data.get("created_by"))
            )

        data["total_record"] = len(advice)
        advice, data = filtering_query(advice, query_string, "advice_id", "ADVICE")

    except AdviceModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = AdviceSerializers(advice, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


class AdviceGroupAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["advice_group"]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            advice_group = AdviceGroupModel.objects.filter(pk=id).first()
        except AdviceGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = AdviceGroupSerializers(advice_group, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("advice_group", "delete")
def delete_group(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        advice_group = AdviceGroupModel.objects.filter(advice_group_id__in=del_id["id"])
    except AdviceGroupModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = advice_group.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("advice_group", "add")
def create_group(request):
    data = {}
    if request.method == "POST":
        advice_group = AdviceGroupModel()
        serializer = AdviceGroupSerializers(advice_group, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("advice_group", "change")
def patch_group(request, id):
    data = {}
    try:
        if id:
            advice_group = AdviceGroupModel.objects.get(pk=id)
        else:
            advice_group = AdviceGroupModel.objects.filter(deleted=0)
    except AdviceGroupModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = AdviceGroupSerializers(advice_group, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("advice_group", "view")
# ================= Retrieve Single or Multiple records=========================
def get_group(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            advice_group = AdviceGroupModel.objects.filter(pk=id, deleted=0)
        else:
            advice_group = AdviceGroupModel.objects.filter(
                Q(deleted=0, created_by=1)
                | Q(created_by=request.data.get("created_by"))
            )

        data["total_record"] = len(advice_group)
        advice_group, data = filtering_query(
            advice_group, query_string, "advice_group_id", "ADVICEGROUP"
        )

    except AdviceGroupModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = AdviceGroupSerializers(advice_group, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
