from decouple import config
from django.core.paginator import Paginator


def pagination(recordset, page):
    warning = None
    p = Paginator(recordset, int(config('PAGE_LIMIT')))
    if int(page) <= int(p.num_pages):
        recordset = p.page(page)
    elif int(page) > int(p.num_pages):
        warning = "You have reached to last page"
        recordset = p.page(p.num_pages)
    elif int(page) < 1:
        recordset = p.page(1)
        warning = "You have reached to first page"
    else:
        recordset = p.page(page)
    return recordset, warning


