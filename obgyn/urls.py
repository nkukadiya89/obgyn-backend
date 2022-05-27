"""obgyn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from user.user_views import CustomTokenObtainPairView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('gettoken/', CustomTokenObtainPairView.as_view(), name="get_token"),
    path('refreshtoken/', TokenRefreshView.as_view(), name="refresh_token"),
    path('verifytoken/', TokenVerifyView.as_view(), name="verify_token"),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('city/', include('city.urls')),
    path('taluka/', include('taluka.urls')),
    path('district/', include('district.urls')),
    path('state/', include('state.urls')),
    path('language/', include('language.urls')),
    path('medicine/', include('medicine.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('surgical-item/', include('surgical_item.urls')),
    path('m-fields/', include('manage_fields.urls')),
    path('advice/', include('advice.urls')),
    path('patient/', include('patient.urls')),
    path('opd/', include('patient_opd.urls')),
    path('report/', include('reports.urls')),
    path('subscription/', include('subscription.urls')),
    path('template-header/', include('template_header.urls')),
    path('subscription_purchase/', include('subscription_purchase.urls')),
    path('obgyn_config/', include('obgyn_config.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

