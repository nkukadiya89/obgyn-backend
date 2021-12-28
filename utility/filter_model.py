import re

from django.db.models import Q



def camel_to_snake(variable_name):
    variable_name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
    return variable_name


class ModelFilterUSER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "first_name":
                model = model.filter(first_name__iexact=fld_value)
            if fld_name == "middle_name":
                model = model.filter(middle_name__iexact=fld_value)
            if fld_name == "last_name":
                model = model.filter(last_name__iexact=fld_value)
            if fld_name == "user_type":
                model = model.filter(user_type__iexact=fld_value)
            if fld_name == "hospital_name":
                model = model.filter(hospital_name__iexact=fld_value)
            if fld_name == "phone":
                model = model.filter(phone=fld_value)
            if fld_name == "state_id":
                model = model.filter(state_id=fld_value)
            if fld_name == "city_id":
                model = model.filter(city_id=fld_value)
            if fld_name == "area_id":
                model = model.filter(area_id=fld_value)
            if fld_name == "pincode":
                model = model.filter(pincode=fld_value)
            if fld_name == "email":
                model = model.filter(email__iexact=fld_value)
            if fld_name == "landline":
                model = model.filter(landline=fld_value)
            if fld_name == "fax_number":
                model = model.filter(fax_number=fld_value)
            if fld_name == "degree":
                model = model.filter(degree__iexact=fld_value)
            if fld_name == "speciality":
                model = model.filter(speciality__iexact=fld_value)
            if fld_name == "aadhar_card":
                model = model.filter(aadhar_card__iexact=fld_value)
            if fld_name == "registration_no":
                model = model.filter(registration_no=fld_value)
            if fld_name == "defaultLanguage_id":
                model = model.filter(default_language_id=fld_value)
            if fld_name == "designation":
                model = model.filter(designation__iexact=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(user_type__icontains=search) |
                Q(hospital_name__icontains=search) |
                Q(state__state_name__icontains=search) |
                Q(city__city_name__icontains=search) |
                Q(email__icontains=search) |
                Q(landline__icontains=search) |
                Q(fax_number__icontains=search) |
                Q(degree__icontains=search) |
                Q(speciality__icontains=search) |
                Q(aadhar_card__icontains=search) |
                Q(registration_no__icontains=search) |
                Q(default_language__language__icontains=search) |
                Q(designation__icontains=search) |
                Q(username__icontains=search)
            )
        return model


class ModelFilterCITY:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "city_name":
                model = model.filter(city_name__iexact=fld_value)
            if fld_name == "state_id":
                model = model.filter(state_id=fld_value)
            if fld_name == "city_id":
                model = model.filter(city_id=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(city_name__icontains=search) |
                Q(state__state_name__icontains=search)
            )
        return model
