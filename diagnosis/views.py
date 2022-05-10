import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db.models import Q

from .models import DiagnosisModel
from .serializers import DiagnosisSerializers
from utility.search_filter import filtering_query
from utility.decorator import validate_permission_id,validate_permission



class DiagnosisAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            diagnosis = DiagnosisModel.objects.filter(pk=id).first()
        except DiagnosisModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = DiagnosisSerializers(diagnosis, request.data)
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
@validate_permission("diagnosis","delete")
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        diagnosis = DiagnosisModel.objects.filter(diagnosis_id__in=del_id["id"])
    except DiagnosisModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = diagnosis.delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("diagnosis","add")
def create(request):
    data = {}
    if request.method == "POST":
        diagnosis = DiagnosisModel()
        serializer = DiagnosisSerializers(diagnosis, data=request.data)
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
@validate_permission_id("diagnosis","change")
def patch(request, id):
    data = {}

    try:
        if id:
            diagnosis = DiagnosisModel.objects.get(pk=id)
        else:
            diagnosis = DiagnosisModel.objects.filter(deleted=0)
    except DiagnosisModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = DiagnosisSerializers(diagnosis, request.data, partial=True)

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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("diagnosis","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            diagnosis = DiagnosisModel.objects.filter(pk=id, deleted=0)
        else:
            diagnosis = DiagnosisModel.objects.filter(Q(deleted=0, created_by=1)  | Q(created_by=request.data.get('created_by')))
        data["total_record"] = len(diagnosis)
        diagnosis, data = filtering_query(diagnosis, query_string, "diagnosis_id", "DIAGNOSIS")

    except DiagnosisModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = DiagnosisSerializers(diagnosis, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
