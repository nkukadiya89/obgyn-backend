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

from patient_opd.models import PatientOpdModel
from .models import PatientDischargeModel
from .serializers import PatientDischargeSerializers
from utility.search_filter import filtering_query
from utility.decorator import validate_permission, validate_permission_id


class PatientDischargeAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_discharge = PatientDischargeModel.objects.filter(pk=id).first()
        except PatientDischargeModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientDischargeSerializers(patient_discharge, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_discharge", "change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_discharge = PatientDischargeModel.objects.filter(
            patient_discharge_id__in=del_id["id"]
        )
    except PatientDischargeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_discharge.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_discharge", "add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        patient_discharge = PatientDischargeModel()
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]
        serializer = PatientDischargeSerializers(patient_discharge, data=request.data)

        if serializer.is_valid():
            serializer.save()
            patient_opd = PatientOpdModel.objects.filter(
                pk=request.data["patient_opd_id"]
            ).first()
            patient_opd.status = "discharge"
            patient_opd.save()

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
@validate_permission_id("patient_discharge","change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient_discharge = PatientDischargeModel.objects.get(pk=id,deleted=0)
        else:
            patient_discharge = PatientDischargeModel.objects.filter(deleted=0)
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except PatientDischargeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientDischargeSerializers(
            patient_discharge, request.data, partial=True
        )

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
@validate_permission("patient_discharge","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            patient_discharge = PatientDischargeModel.objects.filter(pk=id, deleted=0)
        else:
            patient_discharge = PatientDischargeModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_discharge)
        patient_discharge, data = filtering_query(
            patient_discharge, query_string, "patient_discharge_id", "PATIENTDISCHARGE"
        )

    except PatientDischargeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientDischargeSerializers(patient_discharge, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
