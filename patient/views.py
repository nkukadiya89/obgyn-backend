import json

from django.db.models import Q
from django.db.models.functions import Lower
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import (
    JWTAuthentication,
    JWTTokenUserAuthentication,
)

from user.models import User
from utility.aws_file_upload import upload_barcode_image
from utility.decorator import validate_permission, validate_permission_id
from utility.search_filter import filtering_query

from .models import PatientModel
from .serializers import DynamicFieldModelSerializer, PatientSerializers


class PatientAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient = PatientModel.objects.filter(pk=id).first()
        except PatientModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientSerializers(patient, request.data)
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
@validate_permission("patient", "change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    try:
        patient = PatientModel.objects.filter(patient_id__in=del_id["id"])
    except PatientModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        for each_patient in patient:
            each_patient.deleted = 1
            each_patient.save()

        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = 1
        return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient", "add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        patient = PatientModel()
        serializer = PatientSerializers(patient, data=json.loads(request.data["data"]))
        if serializer.is_valid():
            # patient_opd = PatientOpdModel.objects.filter(patient_id=patient.patient_id).first()
            # patient_opd.patient_type = patient.patient_type
            # patient.save()

            serializer.save()
            patient.registered_no = (
                str(now().day)
                + str("{:0>2}".format(now().month))
                + str(now().year)[::3]
                + str(now()).split(" ")[1].split(".")[0].replace(":", "")
            )

            patient.save()
            user = User.objects.filter(pk=patient.user_ptr_id).first()
            if user != None:
                user.set_password(request.POST.get("password"))
                user.save()
                # generate_patient_user_code(user)

            if "media" in request.data:
                if request.data["media"]:
                    if len(request.data["media"]) > 0:
                        file = request.data["media"]
                        patient.upload_file(file)
                        patient.save()

            patient.regd_no_barcode, mob_url = upload_barcode_image(
                patient.registered_no, patient.phone, patient.patient_id
            )
            patient.save()

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
@validate_permission_id("patient", "change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient = PatientModel.objects.get(patient_id=id)
        else:
            patient = PatientModel.objects.filter(deleted=0)
    except PatientModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":

        serializer = PatientSerializers(
            patient, json.loads(request.data["data"]), partial=True
        )

        if serializer.is_valid():
            patient = serializer.save()
            if "media" in request.data:
                if len(request.data["media"]) > 0:
                    file = request.data["media"]
                    patient.upload_file(file)
                    patient.save()

            patient.regd_no_barcode, mob_url = upload_barcode_image(
                patient.registered_no, patient.phone, patient.patient_id
            )
            patient.save()

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
@validate_permission_id("patient", "view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    user_id = request.user.id
    try:
        if id:
            patient = PatientModel.objects.filter(pk=id, deleted=0, created_by=user_id)
        else:
            patient = PatientModel.objects.filter(deleted=0, created_by=user_id)

        data["total_record"] = len(patient)
        patient, data = filtering_query(patient, query_string, "patient_id", "PATIENT")

    except PatientModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientSerializers(patient, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================= Retrieve Single or Multiple records=========================
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@validate_permission_id("patient", "view")
# ================= Retrieve Single or Multiple records=========================
def get_unique_patient(request, id=None):
    query_string = request.query_params
    if "," in query_string["fields"]:
        distinc_key = query_string["fields"].split(",")[1]
    else:
        distinc_key = query_string["fields"]

    if "search" in query_string:
        search_val = query_string["search"].split("=")[0]
    data = {}
    try:
        if id:
            patient = PatientModel.objects.filter(pk=id, deleted=0).order_by(
                Lower(distinc_key)
            )
        else:
            patient = PatientModel.objects.filter(
                Q(deleted=0, created_by=1) | Q(created_by=request.user.id, deleted=0)
            )

        data["total_record"] = len(patient)
        search_string = (
            "patient.filter(" + distinc_key + "__icontains='" + search_val + "')"
        )
        patient = eval(search_string)
        patient = patient.distinct(distinc_key)
    except PatientModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = DynamicFieldModelSerializer(
            patient, many=True, fields=query_string["fields"]
        )

        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
