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
from .models import PatientIndoorModel, IndoorAdviceModel
from .serializers import PatientIndoorSerializers, IndoorAdviceSerializers
from .utils_views import indoor_advice_insert


class PatientIndoorAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            patient_indoor = PatientIndoorModel.objects.filter(pk=id).first()
        except PatientIndoorModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = PatientIndoorSerializers(patient_indoor, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode("utf-8"))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            patient_indoor = PatientIndoorModel.objects.filter(
                patient_indoor_id__in=del_id["id"]
            )
        except PatientIndoorModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = patient_indoor.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            patient_indoor = PatientIndoorModel()
            if "patient_opd_id" not in request.data:
                data["success"] = False
                data["msg"] = "OPD is required"
                data["data"] = request.data
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data["patient_opd"] = request.data["patient_opd_id"]
            serializer = PatientIndoorSerializers(patient_indoor, data=request.data)

            if serializer.is_valid():
                serializer.save()

                if "advice_lst" in request.data:
                        indoor_advice_insert(request,serializer.data["patient_indoor_id"])
                serializer = PatientIndoorSerializers(patient_indoor)

                patient_opd = PatientOpdModel.objects.filter(
                    pk=request.data["patient_opd_id"]
                ).first()
                patient_opd.status = "indoor"
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
@permission_classes([IsAuthenticated])
def patch(request, id):
    data = {}
    try:
        if id:
            patient_indoor = PatientIndoorModel.objects.get(pk=id)
        else:
            patient_indoor = PatientIndoorModel.objects.filter(deleted=0)

        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except PatientIndoorModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = PatientIndoorSerializers(
            patient_indoor, request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            if "advice" in request.data:
                print("value of advice", request.data.get("advice"))
                if request.data.get("advice"):
                    indoor_advice_insert(
                        request.data.get("advice"),
                        serializer.data["patient_indoor_id"],
                        request.data.get("created_by"),
                    )
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
@permission_classes([IsAuthenticatedOrReadOnly])
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            patient_indoor = PatientIndoorModel.objects.filter(pk=id, deleted=0)
        else:
            patient_indoor = PatientIndoorModel.objects.filter(deleted=0)

        data["total_record"] = len(patient_indoor)
        patient_indoor, data = filtering_query(
            patient_indoor, query_string, "patient_indoor_id", "PATIENTINDOOR"
        )

    except PatientIndoorModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = PatientIndoorSerializers(patient_indoor, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)


# ================ INDOOR ADVICE ===============================
class IndoorAdviceAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            indoor_advice = IndoorAdviceModel.objects.filter(pk=id).first()
        except IndoorAdviceModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = IndoorAdviceSerializers(indoor_advice, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode("utf-8"))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            indoor_advice = IndoorAdviceModel.objects.filter(
                indoor_advice_id__in=del_id["id"]
            )
        except IndoorAdviceModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = indoor_advice.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            indoor_advice = IndoorAdviceModel()
            serializer = IndoorAdviceSerializers(indoor_advice, data=request.data)

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
@permission_classes([IsAuthenticated])
def indoor_advice_patch(request, id):
    data = {}
    try:
        if id:
            indoor_advice = IndoorAdviceModel.objects.get(pk=id)
        else:
            indoor_advice = IndoorAdviceModel.objects.filter(deleted=0)
    except IndoorAdviceModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = IndoorAdviceSerializers(indoor_advice, request.data, partial=True)

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
@permission_classes([IsAuthenticatedOrReadOnly])
# ================= Retrieve Single or Multiple records=========================
def indoor_advice_get(request, id=None):
    query_string = request.query_params
    data = {}
    try:
        if id:
            indoor_advice = IndoorAdviceModel.objects.filter(pk=id, deleted=0)
        else:
            indoor_advice = IndoorAdviceModel.objects.filter(deleted=0)

        data["total_record"] = len(indoor_advice)
        indoor_advice, data = filtering_query(
            indoor_advice, query_string, "indoor_advice_id", "INDOORADVICE"
        )

    except IndoorAdviceModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = IndoorAdviceSerializers(indoor_advice, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
