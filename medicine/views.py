from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import MedicineModel, TimingModel, MedicineTypeModel
from .serializers import MedicineSerializers, MedicineTypeSerializers, TimingSerializers


class MedicineAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                medicine = MedicineModel.objects.filter(pk=id)
            else:
                medicine = MedicineModel.objects.all()
        except MedicineModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = MedicineSerializers(medicine, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            medicine = MedicineModel.objects.filter(pk=id).first()
        except MedicineModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = MedicineSerializers(medicine, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        try:
            if id:
                medicine = MedicineModel.objects.get(medicine_id=id)
            else:
                medicine = MedicineModel.objects.all()
        except MedicineModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = MedicineSerializers(medicine, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            medicine = MedicineModel.objects.get(pk=id)
        except MedicineModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            medicine.deleted = 1
            medicine.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            medicine = MedicineModel()
            serializer = MedicineSerializers(medicine, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineTypeAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                medicine_type = MedicineTypeModel.objects.filter(pk=id)
            else:
                medicine_type = MedicineTypeModel.objects.all()
        except MedicineTypeModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = MedicineTypeSerializers(medicine_type, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            medicine_type = MedicineTypeModel.objects.filter(pk=id).first()
        except MedicineTypeModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = MedicineTypeSerializers(medicine_type, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        try:
            if id:
                medicine_type = MedicineTypeModel.objects.get(medicine_type_id=id)
            else:
                medicine_type = MedicineTypeModel.objects.all()
        except MedicineTypeModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = MedicineTypeSerializers(medicine_type, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            medicine_type = MedicineTypeModel.objects.get(pk=id)
        except MedicineTypeModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            medicine_type.deleted = 1
            medicine_type.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            medicine_type = MedicineTypeModel()
            serializer = MedicineTypeSerializers(medicine_type, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimingAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                timing = TimingModel.objects.filter(pk=id)
            else:
                timing = TimingModel.objects.all()
        except TimingModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = TimingSerializers(timing, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            timing = TimingModel.objects.filter(pk=id).first()
        except TimingModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = TimingSerializers(timing, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        try:
            if id:
                timing = TimingModel.objects.get(timing_id=id)
            else:
                timing = TimingModel.objects.all()
        except TimingModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = TimingSerializers(timing, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            timing = TimingModel.objects.get(pk=id)
        except TimingModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            timing.deleted = 1
            timing.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            timing = TimingModel()
            serializer = TimingSerializers(timing, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
