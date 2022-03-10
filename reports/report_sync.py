import pdfkit
from django.http import HttpResponse
from django.shortcuts import render


def download_report(request, base_url, report_name, paper_size="A4", orientation="Portrait"):
    if not orientation in ["Portrait", "Landscape"]:
        orientation = "Portrait"

    url = "".join(["http://", request.get_host(), base_url])

    options = {'page-size': paper_size, 'encoding': "UTF-8", 'orientation': orientation}

    pdf = pdfkit.from_url(url, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + report_name + '"'
    return response


def view_report(request, id):
    return render(request, template_name, context)
