import pdfkit
from django.http import HttpResponse
from django.shortcuts import render



def download_report(request, id):
    url = "".join(["https://", request.get_host(), "/invoice/view/", id])

    options = {'disable-smart-shrinking': ''}


    pdf = pdfkit.from_url(url, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


def view_report(request, id):
    return render(request, template_name, context)
