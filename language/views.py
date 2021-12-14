from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import LanguageModel
from .serializers import LanguageSerializers


class LanguageAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                language = LanguageModel.objects.filter(pk=id)
            else:
                language = LanguageModel.objects.all()
        except LanguageModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = LanguageSerializers(language, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            language = LanguageModel.objects.filter(pk=id).first()
        except LanguageModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = LanguageSerializers(language, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        data = {}

        try:
            if id:
                language = LanguageModel.objects.get(language_id=id)
            else:
                language = LanguageModel.objects.all()
        except LanguageModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = LanguageSerializers(language, request.data, partial=True)

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

    # ================= Delete Record =========================
    def delete(self, request, id):
        data = {}
        try:
            language = LanguageModel.objects.get(pk=id)
        except LanguageModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            language.deleted = 1
            language.save()
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            language = LanguageModel()
            serializer = LanguageSerializers(language, data=request.data)

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
