from .models import Subscription_purchaseModel
from financial_year.models import FinancialYearModel
from django.utils.timezone import now
from django.db.models import Q


def generate_invoice_no():
    sub_cnt = Subscription_purchaseModel.objects.filter(deleted=0).order_by('-subscription_purchase_id').first()

    fy = FinancialYearModel.objects.filter(start_date__lte=now(), end_date__gte=now()).values_list(
        'financial_year').first()

    if fy[0] == sub_cnt.inv_year:
        invoice_no = sub_cnt.invoice_no + 1
    else:
        invoice_no = 1

    return invoice_no, fy[0]

