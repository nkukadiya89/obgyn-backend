from patient_voucher.models import VoucherItemModel


def delete_child_records(surgical_item_list):
    for surgical_item in surgical_item_list:
        voucher_item = VoucherItemModel.objects.filter(surgical_item=surgical_item)
        voucher_item.delete()
