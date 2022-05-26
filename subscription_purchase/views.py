import json

from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from django.db.models import Q
import subscription_purchase

from utility.search_filter import filtering_query
from .models import Subscription_purchaseModel
from .serializers import Subscription_PurchaseSerializers
from utility.decorator import validate_permission, validate_permission_id

class Subscription_purchaseAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            city = Subscription_purchaseModel.objects.filter(pk=id).first()
        except Subscription_purchaseModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = Subscription_PurchaseSerializers(city, request.data)
            if serializer.is_valid():
                serializer.save()
                data["success"] = True
                data["msg"] = "Data updated successfully"
                data["data"] = serializer.data
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================= Delete Record =========================
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@validate_permission("Subscription_Purchase","change")
def delete_Subscription_purchase(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        subscription_purchase = Subscription_purchaseModel.objects.filter(
            subscription_Purchase_id__in=del_id["id"])
    except Subscription_purchaseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        result = subscription_purchase.delete()
        data["success"] = True
        data["msg"] = "Data deleted successfully."
        data["deleted"] = result
        return Response(data=data, status=status.HTTP_200_OK)

# ================= Create New Record=========================
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@validate_permission("Subscription_Purchase","add")
def create_subscription_purchase(request):
    data = {}
    if request.method == "POST":
        subscription_purchase = Subscription_purchaseModel()
        serializer = Subscription_PurchaseSerializers(subscription_purchase, data=request.data)

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
@validate_permission_id("Subscription_Purchase","change")
def patch_subscription_purchase(request, id):
    data = {}
    try:
        if id:
            subscription_purchase = Subscription_purchaseModel.objects.get(pk=id)
        else:
            subscription_purchase = Subscription_purchaseModel.objects.filter(deleted=0)
    except Subscription_purchaseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        serializer = Subscription_PurchaseSerializers(subscription_purchase, request.data, partial=True)

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


# ================= Retrieve Single or Multiple records=========================
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("subscription_Purchase","view")
def get_subscription_purchase(request, id=None):
    query_string = request.query_params

    data = {}
    try:
        if id:
            subscription_purchase = Subscription_purchaseModel.objects.filter(pk=id, deleted=0)
        else:
            subscription_purchase = Subscription_purchaseModel.objects.filter(Q(created_by=1,deleted=0) | Q(created_by=request.data.get('created_by')))

        data["total_record"] = len(subscription_purchase)

        subscription_purchase, data = filtering_query(
            subscription_purchase, query_string, "subscription_Purchase_id", "SUBSCRIPTION_PURCHASE")

    except Subscription_purchaseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = Subscription_PurchaseSerializers(subscription_purchase, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)
