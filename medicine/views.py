import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import MedicineModel, TimingModel, MedicineTypeModel
from .serializers import MedicineSerializers, MedicineTypeSerializers, TimingSerializers


class MedicineAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                medicine = MedicineModel.objects.filter(pk=id)
            else:
                medicine = MedicineModel.objects.all()
        except MedicineModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            serilizer = MedicineSerializers(medicine, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            medicine = MedicineModel.objects.filter(pk=id).first()
        except MedicineModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = MedicineSerializers(medicine, request.data)
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
            medicine = MedicineModel.objects.get(medicineId__in=del_id["id"])
        except MedicineModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = medicine.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            medicine = MedicineModel()
            serializer = MedicineSerializers(medicine, data=request.data)

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


class MedicineTypeAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                medicine_type = MedicineTypeModel.objects.filter(pk=id)
            else:
                medicine_type = MedicineTypeModel.objects.all()
        except MedicineTypeModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            serilizer = MedicineTypeSerializers(medicine_type, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            medicine_type = MedicineTypeModel.objects.filter(pk=id).first()
        except MedicineTypeModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = MedicineTypeSerializers(medicine_type, request.data)
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
            medicine_type = MedicineTypeModel.objects.get(medicineTypeId__in=del_id["id"])
        except MedicineTypeModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = medicine_type.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            medicine_type = MedicineTypeModel()
            serializer = MedicineTypeSerializers(medicine_type, data=request.data)

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


class TimingAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                timing = TimingModel.objects.filter(pk=id)
            else:
                timing = TimingModel.objects.all()
        except TimingModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            serilizer = TimingSerializers(timing, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            timing = TimingModel.objects.filter(pk=id).first()
        except TimingModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = TimingSerializers(timing, request.data)
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
            timing = TimingModel.objects.get(timingId__in=del_id["id"])
        except TimingModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = timing.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            timing = TimingModel()
            serializer = TimingSerializers(timing, data=request.data)

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
def patch_timing(request, id):
    data = {}

    try:
        if id:
            timing = TimingModel.objects.get(pk=id)
        else:
            timing = TimingModel.objects.all()
    except TimingModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = TimingSerializers(timing, request.data, partial=True)

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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patch_medicine_type(request, id):
    data = {}

    try:
        if id:
            medicine_type = MedicineTypeModel.objects.get(pk=id)
        else:
            medicine_type = MedicineTypeModel.objects.all()
    except MedicineTypeModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = MedicineTypeSerializers(medicine_type, request.data, partial=True)

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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def patch_medicine(request, id):
    data = {}

    try:
        if id:
            medicine = MedicineModel.objects.get(pk=id)
        else:
            medicine = MedicineModel.objects.all()
    except MedicineModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = MedicineSerializers(medicine, request.data, partial=True)

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
