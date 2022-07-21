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
from .models import PatientReferalModel
from .serializers import PatientReferalSerializers
from utility.search_filter import filtering_query
from utility.decorator import validate_permission, validate_permission_id


class PatientReferalAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_referal = PatientReferalModel.objects.filter(pk=id).first()
        except PatientReferalModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientReferalSerializers(patient_referal, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Delete Record =========================
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_referal","change")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient_referal = PatientReferalModel.objects.filter(patient_referal_id__in=del_id["id"])
    except PatientReferalModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = patient_referal.update(deleted=1)
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("patient_referal","add")
def create(request):
    data = {}
    request.data["created_by"] = request.user.id
    if request.method == "POST":
        patient_referal = PatientReferalModel()
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

        serializer = PatientReferalSerializers(patient_referal, data=request.data)


        if serializer.is_valid():
            serializer.save()
            patient_opd = PatientOpdModel.objects.filter(pk=request.data["patient_opd_id"]).first()
            patient_opd.status = "referal"
            patient_opd.save()

            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_201_CREATED)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("patient_referal","change")
def patch(request, id):
    data = {}
    request.data["created_by"] = request.user.id
    try:
        if id:
            patient_referal = PatientReferalModel.objects.get(pk=id, deleted=0)
        else:
            patient_referal = PatientReferalModel.objects.filter(deleted=0)

        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except PatientReferalModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientReferalSerializers(patient_referal, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            data["success"] = True
            data["msg"] = "Data updated successfully"
            data["data"] = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)

        data["success"] = False
        data["msg"] = {err_obj: str(serializer.errors[err_obj][0]) for err_obj in serializer.errors}
        data["data"] = []
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("patient_referal","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            patient_referal = PatientReferalModel.objects.filter(pk=id,deleted=0)
        else:
            patient_referal = PatientReferalModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_referal)
        patient_referal, data = filtering_query(patient_referal, query_string, "patient_referal_id", "PATIENTREFERAL")

    except PatientReferalModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientReferalSerializers(patient_referal, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
