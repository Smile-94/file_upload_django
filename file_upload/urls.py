from django.urls import path
from .views import ProductUploadView

app_name = 'file_upload'

urlpatterns = [
    path("product/", ProductUploadView.as_view(), name='product_upload')
]