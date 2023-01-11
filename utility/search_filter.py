from decouple import config
from django.core.paginator import Paginator

from utility.filter_model import *


def camel_to_snake(variable_name):
    variable_name = re.sub(r"(?<!^)(?=[A-Z])", "_", variable_name).lower()
    return variable_name


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

    return recordset, warning


def user_filtering_query(model, query_string, model_id, classnm):
    func_name_filter = "ModelFilter" + classnm + "().filter_fields"
    func_name_search = "ModelFilter" + classnm + "().search"
    data = {}

    if "orderBy" not in query_string:
        orderby = model_id
    else:
        orderby = str(query_string["orderBy"])

    if "sortBy" not in query_string:
        sortby = ""
    else:
        sortby = str(query_string["sortBy"])
        if sortby.lower() == "desc":
            sortby = "-"
        else:
            sortby = ""

    if "filter" in query_string:
        filter = list(query_string["filter"].split(","))
        if filter:
            model = eval(func_name_filter + "(model, filter)")
    if "search" in query_string:
        model = eval(func_name_search + "(model, query_string)")

    if orderby:
        if sortby:
            orderby = sortby + orderby
        model = model.order_by(orderby)

    data["total_record"] = len(model)
    data["current_page"] = 1

    if "page" in query_string:
        if "pageRecord" in query_string:
            pageRecord = query_string["pageRecord"]
        else:
            pageRecord = config("PAGE_LIMIT")
        model, data["warning"] = pagination(model, query_string["page"], pageRecord)

        data["current_page"] = int(query_string["page"])
    return model, data


def filtering_query(model, query_string, model_id, classnm):
    func_name_filter = "ModelFilter" + classnm + "().filter_fields"
    func_name_search = "ModelFilter" + classnm + "().search"
    data = {}

    if "orderBy" not in query_string:
        orderby = model_id
    else:
        orderby = str(query_string["orderBy"])

    if "sortBy" not in query_string:
        sortby = ""
    else:
        sortby = str(query_string["sortBy"])
        if sortby.lower() == "desc":
            sortby = "-"
        else:
            sortby = ""

    data["total_record"] = len(model)
    data["current_page"] = 1

    if "filter" in query_string:
        filter = list(query_string["filter"].split(","))
        if filter:
            model = eval(func_name_filter + "(model, filter)")
            data["total_record"] = len(model)
    if "search" in query_string:
        model = eval(func_name_search + "(model, query_string)")
        data["total_record"] = len(model)
    if orderby:
        if sortby:
            orderby = sortby + orderby
        model = model.order_by(orderby)

    if len(model) > 0:
        model = model.distinct()

    if "page" in query_string:
        if "pageRecord" in query_string:
            pageRecord = query_string["pageRecord"]
        else:
            pageRecord = config("PAGE_LIMIT")
        model, data["warning"] = pagination(model, query_string["page"], pageRecord)

    return model, data
