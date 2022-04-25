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
from .models import PatientUSGFormModel, USGFormChildModel
from .serializers import PatientUSGFormSerializers, USGFormChildSerializers
from .util_views import insert_child_usgform
from obgyn_config.views import update_obgyn_config


class PatientUSGFormAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_usgform = PatientUSGFormModel.objects.filter(pk=id).first()
        except PatientUSGFormModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientUSGFormSerializers(patient_usgform, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            patient_usgform = PatientUSGFormModel.objects.filter(patient_usgform_id__in=del_id["id"])
        except PatientUSGFormModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = patient_usgform.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            patient_usgform = PatientUSGFormModel()
            if "patient_opd_id" not in request.data:
                data["success"] = False
                data["msg"] = "OPD is required"
                data["data"] = request.data
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data["patient_opd"] = request.data["patient_opd_id"]
            serializer = PatientUSGFormSerializers(patient_usgform, data=request.data)

            if serializer.is_valid():
                serializer.save()
                if "usg_child" in request.data:
                    insert_child_usgform(request,serializer.data["patient_usgform_id"])
                
                update_obgyn_config(request)
                patient_opd = PatientOpdModel.objects.filter(pk=request.data["patient_opd_id"]).first()
                patient_opd.status = "usgform"
                patient_opd.save()

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
            patient_usgform = PatientUSGFormModel.objects.get(pk=id)
        else:
            patient_usgform = PatientUSGFormModel.objects.filter(deleted=0)
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except PatientUSGFormModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientUSGFormSerializers(patient_usgform, request.data, partial=True)

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
@permission_classes([IsAuthenticatedOrReadOnly])
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_usgform = PatientUSGFormModel.objects.filter(pk=id, deleted=0)
        else:
            patient_usgform = PatientUSGFormModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_usgform)
        patient_usgform, data = filtering_query(patient_usgform, query_string, "patient_usgform_id", "PATIENTUSGFORM")

    except PatientUSGFormModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientUSGFormSerializers(patient_usgform, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


class USGFormChildAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            usgform_child = USGFormChildModel.objects.filter(pk=id).first()
        except USGFormChildModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = USGFormChildSerializers(usgform_child, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            usgform_child = USGFormChildModel.objects.filter(usgform_child_id__in=del_id["id"])
        except USGFormChildModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = usgform_child.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            usgform_child = USGFormChildModel()
            serializer = USGFormChildSerializers(usgform_child, data=request.data)

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
def child_patch(request, id):
    data = {}
    try:
        if id:
            usgform_child = USGFormChildModel.objects.get(pk=id)
        else:
            usgform_child = USGFormChildModel.objects.filter(deleted=0)
    except USGFormChildModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = USGFormChildSerializers(usgform_child, request.data, partial=True)

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
@permission_classes([IsAuthenticatedOrReadOnly])
# ================= Retrieve Single or Multiple records=========================
def child_get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            usgform_child = USGFormChildModel.objects.filter(pk=id, deleted=0)
        else:
            usgform_child = USGFormChildModel.objects.filter(deleted=0)

        data["total_record"] = len(usgform_child)
        usgform_child, data = filtering_query(usgform_child, query_string, "usgform_child_id", "USGFORMCHILD")

    except USGFormChildModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = USGFormChildSerializers(usgform_child, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
