import re

from django.core.paginator import Paginator


def pagination(recordset, page, pageRecord=5):
    warning = None
    p = Paginator(recordset, int(pageRecord))

    if int(page) < 1:
        recordset = p.page(1)
        warning = "You have reached to first page"
    elif int(page) <= int(p.num_pages) and int(page) > 0:
        recordset = p.page(page)
    elif int(page) > int(p.num_pages) and int(page) > 0:
        warning = "You have reached to last page"
        recordset = p.page(p.num_pages)
    else:
        recordset = p.page(page)
    return recordset, warning, p.num_pages


def camel_to_snake(variable_name):
    variable_name = re.sub(r'(?<!^)(?=[A-Z])', '_', variable_name).lower()
    return variable_name
