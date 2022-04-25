from django.shortcuts import render
from user.models import User
from financial_year.models import FinancialYearModel
from django.utils.timezone import now
from patient_usgform.models import PatientUSGFormModel
from obgyn_config.models import ObgynConfigModel
from datetime import date
import calendar 


# Create your views here.


def update_obgyn_config(request):
    user = User.objects.filter(id=request.data.get("user"), user_type="DOCTOR").first()

    if user:
        fy = (
            FinancialYearModel.objects.filter(
                start_date__lte=now(), end_date__gte=now()
            )
            .values_list("fid")
            .first()
        )

        start_date = fy.start_date
        end_date = fy.end_date

        obgyn_config = ObgynConfigModel.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
            user_id=user.id
        )

        month = date.today().month
        year = date.today().year
        _, num_days = calendar.monthrange(2016, 3)
        first_date = date(year, month, 1)
        last_date = date(year, month, num_days)

        usg_form_y = PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=start_date,
            created_at__date__lte=end_date)

        usg_form_m =PatientUSGFormModel.objects.filter(deleted=0,created_at__date__gte=first_date,
            created_at__date__lte=last_date)
 
        if obgyn_config == None:
            obgyn_config = ObgynConfigModel.objects.create(user_id=user.id,created_by=user.id,deleted=0)
        
        if usg_form_y == None:
            obgyn_config.monthly_usg = 1
            obgyn_config.yearly_usg = 1
        else:
            obgyn_config.yearly_usg = user.yearly_usg + 1
            if usg_form_m == None:
                obgyn_config.monthly_usg = 1
            else:
                obgyn_config.monthly_usg = user.monthly_usg + 1
        
        obgyn_config.save()
