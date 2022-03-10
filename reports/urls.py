from django.urls import path
from reports import views


urlpatterns = [
    path('usg-report/<int:id>/<int:language_id>/', views.usg_report, name="usg_report"),
    path('consultation-report/<int:id>/<int:language_id>/', views.consultation_report, name="consultation_report"),
    path('birth-report/<int:id>/<int:language_id>/', views.birth_report, name="birth_report"),
    path('discharge-card-report/<int:id>/<int:language_id>/', views.discharge_report, name="discharge_report"),
    path('mtp-list-report/<int:id>/<int:language_id>/', views.mtp_list_report, name="mtp_list_report"),
    path('referal-slip-report/<int:id>/<int:language_id>/', views.referal_slip_report, name="referal_slip_report"),
    path('download-report-name/<str:report_name>/<int:id>/<int:language_id>/', views.download_pdf_report, name="download_report"),

    path('view-report/<int:id>/<int:language_id>/', views.view_report, name="view_report"),

]