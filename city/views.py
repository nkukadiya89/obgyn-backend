from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import CityModel
from .serializers import CitySerializers


class CityAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                city = CityModel.objects.filter(pk=id)
            else:
                city = CityModel.objects.all()
        except CityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = CitySerializers(city, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            city = CityModel.objects.filter(pk=id).first()
        except CityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = CitySerializers(city, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Complete Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        print(id)
        try:
            if id:
                city = CityModel.objects.get(city_id=id)
            else:
                city = CityModel.objects.all()
        except CityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = CitySerializers(city, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Partial Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            city = CityModel.objects.get(pk=id)
        except CityModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            city.deleted = 1
            city.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            city = CityModel()
            serializer = CitySerializers(city, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
