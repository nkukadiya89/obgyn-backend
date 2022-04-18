import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from patient.models import PatientModel
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from patient_opd.models import PatientOpdModel
from utility.search_filter import filtering_query
from .models import ConsultationModel
from .serializers import ConsultationSerializers
from .utils_view import add_medicine_for_consultaion



class ConsultationAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    search_fields = ["consultation_name"]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            consultation = ConsultationModel.objects.filter(pk=id).first()
        except ConsultationModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = ConsultationSerializers(consultation, request.data)
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
            consultation = ConsultationModel.objects.filter(consultation_id__in=del_id["id"])
        except ConsultationModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = consultation.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            consultation = ConsultationModel()
            if "patient_opd_id" not in request.data:
                data["success"] = False
                data["msg"] = "OPD is required"
                data["data"] = request.data
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data["patient_opd"] = request.data["patient_opd_id"]
            serializer = ConsultationSerializers(consultation, data=request.data)

            if serializer.is_valid():
                serializer.save()
                patient_opd = PatientOpdModel.objects.filter(pk=request.data["patient_opd_id"]).first()
                patient_opd.status = "consultation"
                patient_opd.save()

                PatientModel.objects.filter(registered_no=request.data["regd_no"]).update(first_edd=request.data["first_edd"])

                if "medicine" in request.data:
                    add_medicine_for_consultaion(request, serializer.data["consultation_id"])

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
            consultation = ConsultationModel.objects.get(pk=id)
        else:
            consultation = ConsultationModel.objects.filter(deleted=0)
        if "patient_opd_id" not in request.data:
            data["success"] = False
            data["msg"] = "OPD is required"
            data["data"] = request.data
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.data["patient_opd"] = request.data["patient_opd_id"]

    except ConsultationModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = ConsultationSerializers(consultation, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            PatientModel.objects.filter(registered_no=request.data["regd_no"]).update(first_edd=request.data["first_edd"])

            if "medicine" in request.data:
                add_medicine_for_consultaion(request, serializer.data["consultation_id"])

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
            consultation = ConsultationModel.objects.filter(pk=id, deleted=0)
        else:
            consultation = ConsultationModel.objects.filter(deleted=0)

        data["total_record"] = len(consultation)
        consultation, data = filtering_query(consultation, query_string, "consultation_id", "CONSULTATION")

    except ConsultationModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = ConsultationSerializers(consultation, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
