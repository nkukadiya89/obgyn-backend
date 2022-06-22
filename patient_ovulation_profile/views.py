import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from patient_opd.models import PatientOpdModel
from utility.search_filter import filtering_query
from .models import PatientOvulationProfileModel
from .serializers import PatientOvulationProfileSerializers
from utility.decorator import validate_permission_id,validate_permission


class PatientOvulationProfileAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(pk=id).first()
        except PatientOvulationProfileModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientOvulationProfileSerializers(patient_ovulation_profile, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_ovulation_profile","change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))

    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(patient_ovulation_profile_id__in=del_id["id"])
    except PatientOvulationProfileModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_ovulation_profile.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_ovulation_profile","add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        patient_ovulation_profile = PatientOvulationProfileModel()
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

        serializer = PatientOvulationProfileSerializers(patient_ovulation_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            patient_opd = PatientOpdModel.objects.filter(pk=request.data["patient_opd_id"]).first()
            patient_opd.status = "ovulation_profile"
            patient_opd.save()

            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(deleted=0, regd_no=serializer.data["regd_no"]).order_by('-created_at')
            serializer = PatientOvulationProfileSerializers(patient_ovulation_profile, many=True)

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
@validate_permission_id("patient_ovulation_profile","change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient_ovulation_profile = PatientOvulationProfileModel.objects.get(pk=id, deleted=0)
        else:
            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(deleted=0)
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except PatientOvulationProfileModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientOvulationProfileSerializers(patient_ovulation_profile, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(deleted=0, regd_no=serializer.data["regd_no"]).order_by('-created_at')
            serializer = PatientOvulationProfileSerializers(patient_ovulation_profile, many=True)

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
@validate_permission_id("patient_ovulation_profile","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(pk=id, deleted=0)
        else:
            patient_ovulation_profile = PatientOvulationProfileModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_ovulation_profile)
        patient_ovulation_profile, data = filtering_query(patient_ovulation_profile, query_string, "patient_ovulation_profile_id", "PATIENTOVULATIONPROFILE")

    except PatientOvulationProfileModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientOvulationProfileSerializers(patient_ovulation_profile, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)

