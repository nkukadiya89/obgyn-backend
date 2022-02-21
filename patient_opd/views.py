import json

from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from patient.models import PatientModel
from patient.serializers import PatientSerializers
from patient.utility.code_generate import generate_patient_user_code
from user.models import User
from utility.search_filter import filtering_query
from .models import PatientOpdModel
from .serializers import PatientOpdSerializers


class PatientOpdAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["patient_opd_id"]

    # # ================= Update all Fields of a record =========================
    # def update(self, request, id):
    #     data = {}
    #     try:
    #         patient_opd = PatientOpdModel.objects.filter(pk=id).first()
    #     except PatientOpdModel.DoesNotExist:
    #         data["success"] = False
    #         data["msg"] = "Record Does not exist"
    #         data["data"] = []
    #         return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
    #     print("akas")
    #     if request.method == "PUT":
    #         serializer = PatientOpdSerializers(patient_opd, json.loads(request.data["patient_opd"]))
    #         patient_serializer = PatientSerializers(patient, json.loads(request.data["patient"]))
    #         if serializer.is_valid():
    #             serializer.save()
    #             print("opd updated")
    #
    #             if patient_serializer.is_valid():
    #                 patient_serializer.save()
    #                 print("patient_updated")
    #             data["success"] = True
    #             data["msg"] = "Data updated successfully"
    #             data["data"] = serializer.data
    #             return Response(data=data, status=status.HTTP_200_OK)
    #
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            patient_opd = PatientOpdModel.objects.filter(patient_opd_id__in=del_id["id"])
        except PatientOpdModel:
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

    def post(self, request):
        data = {}
        if request.method == "POST":

            if "regd_no" in json.loads(request.data["data"])["patient_opd"]:
                regd_no = json.loads(request.data["data"])["patient_opd"].get("regd_no")
                if len(regd_no) > 0:
                    patient = PatientModel.objects.get(registered_no=str(regd_no))
                    # print("patient",patient, len(patient))
                    patient_serializer = PatientSerializers(patient, data=json.loads(request.data["data"])["patient"],
                                                            partial=True)
                else:
                    patient = PatientModel()
                    patient_serializer = PatientSerializers(patient, data=json.loads(request.data["data"])["patient"])

            else:
                patient = PatientModel()
                patient_serializer = PatientSerializers(patient, data=json.loads(request.data["data"])["patient"])

            if patient_serializer.is_valid():
                patient_serializer.save()
                if not patient_serializer.partial:
                    patient.registered_no = \
                        str(now()).replace("-", "").replace(":", "").replace(" ", "").replace(".", "").split("+")[0][
                        :16]
                    patient.save()

                user = User.objects.filter(pk=patient.user_ptr_id).first()
                if user != None:
                    user.set_password(request.POST.get("password"))
                    user.save()
                    generate_patient_user_code(user)

                if "media" in request.data:
                    if len(request.data["media"]) > 0:
                        file = request.data["media"]
                        patient.upload_file(file)
                        patient.save()

            else:
                data["success"] = False
                data["msg"] = patient_serializer.errors
                data["data"] = patient_serializer.data
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            opd_data = json.loads(request.data["data"])["patient_opd"]
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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patch(request, id):
    data = {}
    try:
        if id:
            patient_opd = PatientOpdModel.objects.get(pk=id)
            patient = patient_opd.patient
    except PatientOpdModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        # print(request.data["data"]["patient_opd"])
        serializer = PatientOpdSerializers(patient_opd, json.loads(request.data["data"])["patient_opd"], partial=True)
        patient_serializer = PatientSerializers(patient, json.loads(request.data["data"])["patient"], partial=True)

        if serializer.is_valid():
            serializer.save()

            if patient_serializer.is_valid():
                patient_serializer.save()

                if "media" in request.data:
                    if len(request.data["media"]) > 0:
                        file = request.data["media"]
                        patient.upload_file(file)
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_opd = PatientOpdModel.objects.filter(pk=id, deleted=0)
        else:
            patient_opd = PatientOpdModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_opd)
        patient_opd, data = filtering_query(patient_opd, query_string, "patient_opd_id", "PATIENTOPD")

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
