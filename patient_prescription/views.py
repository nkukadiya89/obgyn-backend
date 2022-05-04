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
from utility.search_filter import filtering_query
from .models import PatientPrescriptionModel
from .serializers import PatientPrescriptionSerializers
from utility.decorator import validate_permission


class PatientPrescriptionAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_prescription = PatientPrescriptionModel.objects.filter(
                pk=id
            ).first()
        except PatientPrescriptionModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientPrescriptionSerializers(
                patient_prescription, request.data
            )
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
@validate_permission("patient_prescription", "change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_prescription = PatientPrescriptionModel.objects.filter(
            patient_prescription_id__in=del_id["id"]
        )
    except PatientPrescriptionModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_prescription.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_prescription", "add")
def post(request):
    data = {}
    if request.method == "POST":
        patient_prescription = PatientPrescriptionModel()
        serializer = PatientPrescriptionSerializers(
            patient_prescription, data=request.data
        )

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
@validate_permission("patient_prescription", "change")
def patch(request, id):
    data = {}

    try:
        if id:
            patient_prescription = PatientPrescriptionModel.objects.get(pk=id)
        else:
            patient_prescription = PatientPrescriptionModel.objects.filter(deleted=0)
    except PatientPrescriptionModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientPrescriptionSerializers(
            patient_prescription, request.data, partial=True
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
@validate_permission("patient_prescription", "view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            patient_prescription = PatientPrescriptionModel.objects.filter(
                pk=id, deleted=0
            )
        else:
            patient_prescription = PatientPrescriptionModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_prescription)
        patient_prescription, data = filtering_query(
            patient_prescription,
            query_string,
            "patient_prescription_id",
            "PATIENTPRESCRIPTION",
        )

    except PatientPrescriptionModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientPrescriptionSerializers(patient_prescription, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
