from django.urls import path
from reports import views


urlpatterns = [

    #PRINTABLE REPORT

    path('usg-report/<int:id>/<int:language_id>/', views.usg_report, name="usg_report"),
    path('consultation-report/<int:id>/<int:language_id>/', views.consultation_report, name="consultation_report"),
    path('birth-report/<int:id>/<int:language_id>/', views.birth_report, name="birth_report"),
    path('delivery-report/<int:language_id>/', views.delivery_report, name="delivery_report"),
    path('billing-report/<int:language_id>/', views.billing_report, name="billing_report"),
    path('discharge-card-report/<int:id>/<int:language_id>/', views.discharge_report, name="discharge_report"),
    path('mtp-list-report/<int:language_id>/', views.mtp_list_report, name="mtp_list_report"),
    path('referal-slip-report/<int:id>/<int:language_id>/', views.referal_slip_report, name="referal_slip_report"),
    path('download-report-name/<str:report_name>/<int:id>/<int:language_id>/', views.download_pdf_report, name="download_report"),
    path('daily-opd-income/<int:language_id>/',views.daily_opd_income, name="daily_opd_income"),
    path('hospital-bill/<int:language_id>/<str:bill_no>',views.hospital_bill, name="hospital_bill"),
    path('indoor-case-paper/<int:language_id>/<int:indoor_no>/',views.indoor_case_paper, name="indoor_case_paper"),

    path('view-report/<int:id>/<int:language_id>/', views.view_report, name="view_report"),

    path('update-phone',views.match_regd_no, name="match_phone"),
    ####################################
    
    #DASHBOARD REPORTS
    path('dashboard-api-r1/',views.active_patient,name="dashboard-api-r1"),
    path('dashboard-api-r1/<int:id>',views.active_patient,name="dashboard-api-r1"),

]