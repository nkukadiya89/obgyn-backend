from django.db.models import Q
from rest_framework import serializers
from .models import Subscription_purchaseModel



    

class Subscription_PurchaseSerializers(serializers.ModelSerializer):

    subscription_purchase_id = serializers.IntegerField(read_only=True)


    class Meta:
        model = Subscription_purchaseModel
        fields = ['subscription_purchase_id', 'subscription_date', 'hospital', 'subscription', 'price', 'duration',
                  'start_date', 'over_date', 'description', 'inactive', 'tax_perc', 'invoice_no', 'inv_year','created_by','deleted']