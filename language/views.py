from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import LanguageModel
from .serializers import LanguageSerializers


class LanguageAPI(APIView):
    # authentication_classes = (JWTTokenUserAuthentication,)
    # permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                language = LanguageModel.objects.filter(pk=id)
            else:
                language = LanguageModel.objects.all()
        except LanguageModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = LanguageSerializers(language, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            language = LanguageModel.objects.filter(pk=id).first()
        except LanguageModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = LanguageSerializers(language, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Complete Update successfully"
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        try:
            if id:
                language = LanguageModel.objects.get(language_id=id)
            else:
                language = LanguageModel.objects.all()
        except LanguageModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = LanguageSerializers(language, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Partial Update successfully"
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            language = LanguageModel.objects.get(pk=id)
        except LanguageModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            language.deleted = 1
            language.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            language = LanguageModel()
            serializer = LanguageSerializers(language, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
