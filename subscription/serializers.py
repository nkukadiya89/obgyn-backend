
from django.db.models import Q
from rest_framework import serializers

from .models import SubscriptionModel


class SubscriptionSerializers(serializers.ModelSerializer):
    def validate(self, data):
        subscription_name = data.get('subscription_name')

        if not subscription_name.isalpha():
            raise serializers.ValidationError("Invalid subscription Name")

        duplicate_subscription = SubscriptionModel.objects.filter(deleted=0, subscription_name__iexact=subscription_name)

        if self.partial:
            duplicate_subscription = duplicate_subscription.filter(~Q(pk=self.instance.subscription_id)).first()
        else:
            duplicate_subscription = duplicate_subscription.first()

        if duplicate_subscription != None:
            raise serializers.ValidationError("subscription already exist.")
            
        i = int(data["actual_price"]) * int(data["discount"]) /100
        data["sell_price"] = int(data["actual_price"])-i

        return data

    subscription_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = SubscriptionModel
        fields = ['subscription_id', 'subscription_name', 'actual_price', 'discount', 'sell_price', 'duration', 'description','created_by', 'deleted']
