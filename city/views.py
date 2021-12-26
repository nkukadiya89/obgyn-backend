import json

from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from utility.search_filter import filtering_query
from .models import CityModel
from .serializers import CitySerializers


class CityAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    data = {}
    search_fields = ["city_name"]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        query_string = request.query_params

        try:
            if id:
                city = CityModel.objects.filter(pk=id)
            else:
                city = CityModel.objects.all()

            city, data = filtering_query(city, query_string, "city_id", "CITY")
            data["total_record"] = len(city)

        except CityModel.DoesNotExist:
            self.data["success"] = False
            self.data["msg"] = "Record Does not exist"
            self.data["data"] = []
            return Response(data=self.data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "GET":
            serilizer = CitySerializers(city, many=True)
            self.data["success"] = True
            self.data["msg"] = "OK"
            self.data["data"] = serilizer.data
            return Response(data=self.data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            city = CityModel.objects.filter(pk=id).first()
        except CityModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = CitySerializers(city, request.data)
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
                city = CityModel.objects.get(city_id=id)
            else:
                city = CityModel.objects.all()
        except CityModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PATCH":
            serializer = CitySerializers(city, request.data, partial=True)

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
    def delete(self, request):
        data = {}
        del_id = json.loads(request.body.decode('utf-8'))

        if "id" not in del_id:
            data["success"] = False
            data["msg"] = "Record ID not provided"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        try:
            city = CityModel.objects.filter(city_id__in=del_id["id"])
        except CityModel:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "DELETE":
            result = city.update(deleted=1)
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            data["deleted"] = result
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            city = CityModel()
            serializer = CitySerializers(city, data=request.data)

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

    def filter_fields(self, city, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "city_name":
                city = city.filter(city_name__iexact=fld_value)
            if fld_name == "state_id":
                city = city.filter(state_id=fld_value)

        return city

    def search(self, city, search):
        if search:
            city = city.filter(
                Q(city_name__icontains=search) |
                Q(state__state_name__icontains=search)
            )
        return city
