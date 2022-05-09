from django.urls import path

from .views import (
    PatientVoucherAPI,
    patch,
    get,
    VoucherItemAPI,
    voucher_item_patch,
    voucher_item_get,
    create,
    create_item,
    delete,
    delete_item,
)

urlpatterns = [
    path("<int:id>/", PatientVoucherAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("delete/", delete),
    path("update/<int:id>/", patch),
    path("item/<int:id>/", VoucherItemAPI.as_view()),
    path("item/get/", voucher_item_get),
    path("item/get/<int:id>", voucher_item_get),
    path("item/create/", create_item),
    path("item/delete/", delete_item),
    path("item/update/<int:id>/", voucher_item_patch),
]
