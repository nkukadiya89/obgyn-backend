import json

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import ManageFieldsModel, FieldMasterModel
from .serializers import ManageFieldsSerializers, FieldMasterSerializers
from utility.search_filter import filtering_query
from django.db.models import Q
from utility.decorator import validate_permission


class ManageFieldsAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    queryset = ManageFieldsModel.objects.filter(deleted=0)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            manage_fields = ManageFieldsModel.objects.filter(pk=id).first()
        except ManageFieldsModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = ManageFieldsSerializers(manage_fields, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Delete Record =========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("manage_fields","change")
def delete_mf(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        manage_fields = ManageFieldsModel.objects.filter(mf_id__in=del_id["id"])
    except ManageFieldsModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = manage_fields.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("manage_fields","add")
def create_mf(request):
    data = {}
    if request.method == "POST":
        manage_fields = ManageFieldsModel()
        serializer = ManageFieldsSerializers(manage_fields, data=request.data)

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
@validate_permission("manage_fields","change")
def patch_mf(request, id):
    data = {}

    try:
        if id:
            manage_fields = ManageFieldsModel.objects.get(pk=id, deleted=0)
        else:
            manage_fields = ManageFieldsModel.objects.filter(deleted=0)
    except ManageFieldsModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = ManageFieldsSerializers(manage_fields, request.data, partial=True)

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
@validate_permission("manage_fields","view")
# ================= Retrieve Single or Multiple records=========================
def get_mf(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            manage_fields = ManageFieldsModel.objects.filter(pk=id, deleted=0)
        else:
            manage_fields = ManageFieldsModel.objects.filter(
                Q(deleted=0, created_by=1)
                | Q(created_by=request.data.get("created_by"))
            )

        data["total_record"] = len(manage_fields)
        manage_fields, data = filtering_query(
            manage_fields, query_string, "mf_id", "MANAGEFIELDS"
        )

    except ManageFieldsModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = ManageFieldsSerializers(manage_fields, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


class FieldMasterAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    # permission_classes = [DjangoModelPermissions]

    queryset = FieldMasterModel.objects.filter(deleted=0)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            field_master = FieldMasterModel.objects.filter(pk=id).first()
        except FieldMasterModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = FieldMasterSerializers(field_master, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Delete Record =========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("field_master","change")
def delete_mfm(self, request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        field_master = FieldMasterModel.objects.filter(
            field_master_id__in=del_id["id"]
        )
    except FieldMasterModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = field_master.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("field_master","add")
def create_mfm(request):
    data = {}
    if request.method == "POST":
        field_master = FieldMasterModel()
        serializer = FieldMasterSerializers(field_master, data=request.data)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            all_fields_master = FieldMasterModel.objects.filter(deleted=0).order_by('-created_at')
            all_serilizer = FieldMasterSerializers(all_fields_master, many=True)
            data["data"] = all_serilizer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = serializer.errors
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("field_master","change")
def patch_mfm(request, id):
    data = {}

    try:
        if id:
            field_master = FieldMasterModel.objects.get(pk=id, deleted=0)
        else:
            field_master = FieldMasterModel.objects.filter(deleted=0)
    except FieldMasterModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = FieldMasterSerializers(field_master, request.data, partial=True)

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
@validate_permission("field_master","view")
# ================= Retrieve Single or Multiple records=========================
def get_mfm(request, id=None):

    query_string = request.query_params
    data = {}
    try:
        if id:
            field_master = FieldMasterModel.objects.filter(pk=id, deleted=0)
        else:
            field_master = FieldMasterModel.objects.filter(
                Q(deleted=0, created_by=1)
                | Q(created_by=request.data.get("created_by"))
            )

        data["total_record"] = len(field_master)
        field_master, data = filtering_query(
            field_master, query_string, "field_master_id", "FIELDMASTER"
        )

    except FieldMasterModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = FieldMasterSerializers(field_master, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
