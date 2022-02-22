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

from user.models import User
from utility.search_filter import filtering_query
from .models import PatientModel
from .serializers import PatientSerializers


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
    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))
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
    def post(self, request):
        data = {}
        if request.method == "POST":
            patient = PatientModel()
            serializer = PatientSerializers(patient, data=json.loads(request.data["data"]))

            if serializer.is_valid():
                serializer.save()
                patient.registered_no = \
                    str(now()).replace("-", "").replace(":", "").replace(" ", "").replace(".", "").split("+")[0][:16]

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
            patient = PatientModel.objects.get(patient_id=id)
        else:
            patient = PatientModel.objects.filter(deleted=0)
    except PatientModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":

        serializer = PatientSerializers(patient, json.loads(request.data["data"]), partial=True)

        if serializer.is_valid():
            patient = serializer.save()
            if "media" in request.data:
                if len(request.data["media"]) > 0:
                    file = request.data["media"]
                    patient.upload_file(file)
                    patient.save()

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
            patient = PatientModel.objects.filter(pk=id, deleted=0)
        else:
            patient = PatientModel.objects.filter(deleted=0)

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
