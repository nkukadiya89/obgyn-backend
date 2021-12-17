from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import SurgicalItemModel,SurgicalItemGroupModel
from .serializers import SurgicalItemSerializers, SurgicalItemGroupSerializers


class SurgicalItemAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                surgical_item = SurgicalItemModel.objects.filter(pk=id)
            else:
                surgical_item = SurgicalItemModel.objects.all()
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "GET":
            serilizer = SurgicalItemSerializers(surgical_item, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            surgical_item = SurgicalItemModel.objects.filter(pk=id).first()
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "PUT":
            serializer = SurgicalItemSerializers(surgical_item, request.data)
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
                surgical_item = SurgicalItemModel.objects.get(surgical_item_id=id)
            else:
                surgical_item = SurgicalItemModel.objects.all()
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "PATCH":
            serializer = SurgicalItemSerializers(surgical_item, request.data, partial=True)

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
            surgical_item = SurgicalItemModel.objects.get(pk=id)
        except SurgicalItemModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "DELETE":
            surgical_item.deleted = 1
            surgical_item.save()
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            surgical_item = SurgicalItemModel()
            serializer = SurgicalItemSerializers(surgical_item, data=request.data)

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

class SurgicalItemGroupAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        data = {}
        try:
            if id:
                surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id)
            else:
                surgical_item_group = SurgicalItemGroupModel.objects.all()
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "GET":
            serilizer = SurgicalItemGroupSerializers(surgical_item_group, many=True)
            data["success"] = True
            data["msg"] = "OK"
            data["data"] = serilizer.data
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id).first()
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "PUT":
            serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data)
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
                surgical_item_group = SurgicalItemGroupModel.objects.get(surgical_item_group_id=id)
            else:
                surgical_item_group = SurgicalItemGroupModel.objects.all()
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "PATCH":
            serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data, partial=True)

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
            surgical_item_group = SurgicalItemGroupModel.objects.get(pk=id)
        except SurgicalItemGroupModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_NOT_FOUND)

        if request.method == "DELETE":
            surgical_item_group.deleted = 1
            surgical_item_group.save()
            data["success"] = True
            data["msg"] = "Data deleted successfully."
            return Response(data=data, status=status.HTTP_200_OK)

    # ================= Create New Record=========================
    def post(self, request):
        data = {}
        if request.method == "POST":
            surgical_item_group = SurgicalItemGroupModel()
            serializer = SurgicalItemGroupSerializers(surgical_item_group, data=request.data)

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
