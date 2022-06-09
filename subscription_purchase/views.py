import json

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Subscription_purchaseModel
from .serializers import Subscription_PurchaseSerializers
from utility.search_filter import filtering_query
from utility.decorator import validate_permission, validate_permission_id
from .utils_views import generate_invoice_no

class Subscription_purchaseAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        data = {}
        try:
            subscription_purchase = Subscription_purchaseModel.objects.filter(pk=id).first()
        except Subscription_purchaseModel.DoesNotExist:
            data["success"] = False
            data["msg"] = "Record Does not exist"
            data["data"] = []
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "PUT":
            serializer = Subscription_PurchaseSerializers(subscription_purchase, request.data)
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
def delete(request):
    data = {}
    del_id = json.loads(request.body.decode('utf-8'))
    if "id" not in del_id:
        data["success"] = False
        data["msg"] = "Record ID not provided"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    try:
        subscription_purchase = Subscription_purchaseModel.objects.filter(
            subscription_purchase_id__in=del_id["id"])
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
@validate_permission("subscription_purchase","add")
def create(request):
    data = {}
    if request.method == "POST":
        subscription_purchase = Subscription_purchaseModel()
        serializer = Subscription_PurchaseSerializers(subscription_purchase, data=request.data)

        if serializer.is_valid():
            subscription_purchase = serializer.save()
            # invoice_no, inv_year = generate_invoice_no(serializer.data["subscription_purchase_id"])

            # subscription_purchase.invoice_no=invoice_no
            # subscription_purchase.inv_year = inv_year
            # subscription_purchase.save()

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
def patch(request, id):
    data = {}
    try:
        if id:
            subscription_purchase = Subscription_purchaseModel.objects.get(pk=id, deleted=0)
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@validate_permission_id("subscription_purchase","view")
# ================= Retrieve Single or Multiple records=========================
def get(request, id=None):
    query_string = request.query_params
    data={}
    try:
        if id:
            subscription_purchase = Subscription_purchaseModel.objects.filter(pk=id, deleted=0)
        else:
            subscription_purchase = Subscription_purchaseModel.objects.filter(deleted=0)

        data["total_record"] = len(subscription_purchase)
        subscription_purchase, data = filtering_query(subscription_purchase, query_string, "subscription_purchase_id", "SUBSCRIPTIONPURCHASE")

    except Subscription_purchaseModel.DoesNotExist:
        data["success"] = False
        data["msg"] = "Record Does not exist"
        data["data"] = []
        return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serilizer = Subscription_PurchaseSerializers(subscription_purchase, many=True)
        data["success"] = True
        data["msg"] = "OK"
        data["data"] = serilizer.data
        return Response(data=data, status=status.HTTP_200_OK)
