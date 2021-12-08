from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DiagnosisModel
from .serializers import DiagnosisSerializers
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class DiagnosisAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                diagnosis = DiagnosisModel.objects.filter(pk=id)
            else:
                diagnosis = DiagnosisModel.objects.all()
        except DiagnosisModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = DiagnosisSerializers(diagnosis, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            diagnosis = DiagnosisModel.objects.filter(pk=id).first()
        except DiagnosisModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = DiagnosisSerializers(diagnosis, request.data)
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
                diagnosis = DiagnosisModel.objects.get(diagnosis_id=id)
            else:
                diagnosis = DiagnosisModel.objects.all()
        except DiagnosisModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = DiagnosisSerializers(diagnosis, request.data, partial=True)

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
            diagnosis = DiagnosisModel.objects.get(pk=id)
        except DiagnosisModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            diagnosis.deleted = 1
            diagnosis.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            diagnosis = DiagnosisModel()
            serializer = DiagnosisSerializers(diagnosis, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
