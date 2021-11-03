from os import name
from django.urls import path
from .views import create_certificate, certificate, homepage, add_cert_revocation, cert_revocation_list

app_name = "core"

urlpatterns = [
    path('', homepage, name='homepage'),
    path('create_certificate/', create_certificate, name='create_certificate'),
    path('certificate/', certificate, name='certificate'),
    path('add_cert_revocation/', add_cert_revocation, name='add_cert_revocation'),
    path('cert_revocation_list/', cert_revocation_list, name='cert_revocation_list'),
]
