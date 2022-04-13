from patient_voucher.models import VoucherItemModel
from patient_voucher.serializers import VoucherItemSerializers


def insert_surgical_item(request, patient_voucher_id):
    if "surgical_item" in request.data:
        surgical_item_list = request.data.get('surgical_item')

        surgical_item_dict = {}
        for surgicalitem in surgical_item_list:
            surgical_item_dict["surgical_item"] = surgicalitem["surgical_item"]
            surgical_item_dict["unit"] = surgicalitem["unit"]
            surgical_item_dict["rate"] = surgicalitem["rate"]
            surgical_item_dict["patient_voucher"] = patient_voucher_id
            surgical_item_dict["created_by"] = request.data.get('created_by')

            surgical_item = VoucherItemModel()
            serializer = VoucherItemSerializers(surgical_item, data=surgical_item_dict)
            if serializer.is_valid():
                serializer.save()
