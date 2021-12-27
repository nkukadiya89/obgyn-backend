import re

from django.db.models import Q



def camel_to_snake(variable_name):
    variable_name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
    return variable_name


class ModelFilterUSER:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = camel_to_snake(fields.split("=")[0])
            fld_value = fields.split("=")[1]
            if fld_name == "first_name":
                model = model.filter(first_name__iexact=fld_value)
            if fld_name == "middleName":
                model = model.filter(middleName__iexact=fld_value)
            if fld_name == "last_name":
                model = model.filter(last_name__iexact=fld_value)
            if fld_name == "userType":
                model = model.filter(userType__iexact=fld_value)
            if fld_name == "hospitalName":
                model = model.filter(hospitalName__iexact=fld_value)
            if fld_name == "phone":
                model = model.filter(phone=fld_value)
            if fld_name == "stateId":
                model = model.filter(stateId=fld_value)
            if fld_name == "cityId":
                model = model.filter(cityId=fld_value)
            if fld_name == "areaId":
                model = model.filter(areaId=fld_value)
            if fld_name == "pincode":
                model = model.filter(pincode=fld_value)
            if fld_name == "email":
                model = model.filter(email__iexact=fld_value)
            if fld_name == "landline":
                model = model.filter(landline=fld_value)
            if fld_name == "faxNumber":
                model = model.filter(faxNumber=fld_value)
            if fld_name == "degree":
                model = model.filter(degree__iexact=fld_value)
            if fld_name == "speciality":
                model = model.filter(speciality__iexact=fld_value)
            if fld_name == "aadharCard":
                model = model.filter(aadharCard__iexact=fld_value)
            if fld_name == "registrationNo":
                model = model.filter(registrationNo=fld_value)
            if fld_name == "defaultLanguageId":
                model = model.filter(defaultLanguageId=fld_value)
            if fld_name == "designation":
                model = model.filter(designation__iexact=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middleName__icontains=search) |
                Q(userType__icontains=search) |
                Q(hospitalName__icontains=search) |
                Q(state__stateName__icontains=search) |
                Q(city__cityName__icontains=search) |
                Q(email__icontains=search) |
                Q(landline__icontains=search) |
                Q(faxNumber__icontains=search) |
                Q(degree__icontains=search) |
                Q(speciality__icontains=search) |
                Q(aadharCard__icontains=search) |
                Q(registrationNo__icontains=search) |
                Q(defaultLanguage__language__icontains=search) |
                Q(designation__icontains=search) |
                Q(username__icontains=search)
            )
        return model


class ModelFilterCITY:
    def filter_fields(self, model, filter_fields):
        for fields in filter_fields:
            fld_name = fields.split("=")[0]
            fld_value = fields.split("=")[1]
            if fld_name == "cityName":
                model = model.filter(cityName__iexact=fld_value)
            if fld_name == "stateId":
                model = model.filter(stateId=fld_value)
            if fld_name == "cityId":
                model = model.filter(cityId=fld_value)
        return model

    def search(self, model, query_string):
        search = query_string["search"]
        if search:
            model = model.filter(
                Q(cityName__icontains=search) |
                Q(state__stateName__icontains=search)
            )
        return model
