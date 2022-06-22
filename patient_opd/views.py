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

from patient.models import PatientModel
from patient.serializers import PatientSerializers
from user.models import User
from utility.search_filter import filtering_query
from .models import PatientOpdModel
from .serializers import PatientOpdSerializers
from user.user_views import generate_regd_no
from utility.decorator import validate_permission, validate_permission_id
from utility.aws_file_upload import upload_barcode_image


class PatientOpdAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["patient_opd_id"]


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_opd", "change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode("utf-8"))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_opd = PatientOpdModel.objects.filter(patient_opd_id__in=del_id["id"])
    except PatientOpdModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_opd.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_opd", "add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    gen_regist_no = generate_regd_no()

    if request.method == "POST":
        patient_opd_data = json.loads(request.data["data"])["patient_opd"]
        patient_data = json.loads(request.data["data"])["patient"]
        patient_data["created_by"] = patient_opd_data["created_by"] = request.user.id
        if "phone" in patient_data:
            if len(str(patient_data["phone"])) < 5:
                patient_data["phone"] = "F_" + gen_regist_no
        if "regd_no" in patient_opd_data:
            regd_no = patient_opd_data.get("regd_no")
            if len(regd_no) > 0:
                patient = PatientModel.objects.get(registered_no=str(regd_no))
                patient_serializer = PatientSerializers(
                    patient, data=patient_data, partial=True
                )
            else:
                patient = PatientModel()
                patient_serializer = PatientSerializers(patient, data=patient_data)

        else:
            patient = PatientModel()
            patient_serializer = PatientSerializers(patient, data=patient_data)

        if patient_serializer.is_valid():
            patient_serializer.save()
            if not patient_serializer.partial:
                patient.registered_no = gen_regist_no

                patient.save()

            user = User.objects.filter(pk=patient.user_ptr_id).first()
            if user != None:
                user.set_password(request.POST.get("password"))
                user.save()
                # generate_patient_user_code(user)

            if "media" in request.data:
                if len(request.data["media"]) > 0:
                    file = request.data["media"]
                    patient.upload_file(file)
                    patient.save()
            patient.regd_no_barcode , mob_url= upload_barcode_image(patient.registered_no,patient.phone,patient.patient_id)
            patient.save()
        else:
            data["success"] = False
            data["msg"] = patient_serializer.errors
            data["data"] = patient_serializer.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        opd_data = patient_opd_data
        opd_data["regd_no"] = str(patient.registered_no)

        patient_opd = PatientOpdModel()
        serializer = PatientOpdSerializers(patient_opd, data=opd_data)

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
@validate_permission_id("patient_opd", "change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient_opd = PatientOpdModel.objects.get(pk=id, deleted=0)
            patient = patient_opd.patient
    except PatientOpdModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        patient_opd_data = json.loads(request.data["data"])["patient_opd"]
        patient_data = json.loads(request.data["data"])["patient"]

        patient_opd_data["created_by"] = patient_data["created_by"] = request.user.id

        if patient_data["phone"] == "0" or patient_data["phone"] == "":
            patient_data["phone"] = "F_" + patient_opd_data["regd_no"]


        serializer = PatientOpdSerializers(patient_opd, patient_opd_data, partial=True)
        patient_serializer = PatientSerializers(patient, patient_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            
            if patient_serializer.is_valid():
                patient_serializer.save()

                if "media" in request.data:
                    if len(request.data["media"]) > 0:
                        file = request.data["media"]
                        patient.upload_file(file)
                        patient.save()


                patient.regd_no_barcode, mob_url = upload_barcode_image(patient.registered_no,patient.phone,patient.patient_id)
                patient.save()
            else:
                data["success"] = False
                data["msg"] = patient_serializer.errors
                data["data"] = []
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
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
@validate_permission_id("patient_opd", "view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_opd = PatientOpdModel.objects.filter(pk=id, deleted=0, created_by=request.user.id)
        else:
            patient_opd = PatientOpdModel.objects.filter(deleted=0,created_by = request.user.id)

        data["total_record"] = len(patient_opd)
        patient_opd, data = filtering_query(
            patient_opd, query_string, "patient_opd_id", "PATIENTOPD"
        )

    except PatientOpdModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientOpdSerializers(patient_opd, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
