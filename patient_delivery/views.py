import json

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    JWTTokenUserAuthentication,
)

from obgyn_config.views import get_obgyn_config
from patient_opd.models import PatientOpdModel
from utility.decorator import validate_permission, validate_permission_id
from utility.search_filter import filtering_query

from .models import PatientDeliveryModel
from .serializers import PatientDeliverySerializers, change_payload


class PatientDeliveryAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["patient_delivery_id"]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_delivery = PatientDeliveryModel.objects.filter(pk=id).first()
        except PatientDeliveryModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientDeliverySerializers(patient_delivery, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_delivery", "change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_delivery = PatientDeliveryModel.objects.filter(
            patient_delivery_id__in=del_id["id"]
        )
    except PatientDeliveryModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_delivery.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_delivery", "add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        patient_delivery = PatientDeliveryModel()
        if "sr_no" not in request.data:
            (
                request.data["serial_no_month"],
                request.data["serial_no_year"],
                request.data["sr_no"],
            ) = get_obgyn_config(request.user, PatientDeliveryModel)

        serializer = PatientDeliverySerializers(patient_delivery, data=request.data)

        if serializer.is_valid():
            serializer.save()

            patient_delivery = PatientDeliveryModel.objects.filter(
                deleted=0, regd_no=request.data["regd_no"]
            ).order_by("-created_at")
            serializer = PatientDeliverySerializers(patient_delivery, many=True)

            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = {
            err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors
        }
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("patient_delivery", "change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient_delivery = PatientDeliveryModel.objects.get(pk=id, deleted=0)
        else:
            patient_delivery = PatientDeliveryModel.objects.filter(deleted=0)

    except PatientDeliveryModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        change_payload(request)
        serializer = PatientDeliverySerializers(
            patient_delivery, request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            patient_delivery = PatientDeliveryModel.objects.filter(
                deleted=0, regd_no=request.data["regd_no"]
            ).order_by("-created_at")
            serializer = PatientDeliverySerializers(patient_delivery, many=True)

            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = {
            err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors
        }
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("patient_delivery", "view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_delivery = PatientDeliveryModel.objects.filter(pk=id, deleted=0)
        else:
            patient_delivery = PatientDeliveryModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_delivery)
        patient_delivery, data = filtering_query(
            patient_delivery, query_string, "patient_delivery_id", "PATIENTDELIVERY"
        )

    except PatientDeliveryModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientDeliverySerializers(patient_delivery, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_delivery", "view")
def get_sequence(request):
    data = {}

    data["serial_no_month"], data["serial_no_year"], data["sr_no"] = get_obgyn_config(
        request.user, PatientDeliveryModel
    )

    return Response(data=data, status=status.HTTP_200_OK)
