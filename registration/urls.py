from django.urls import path
from .views import CSVUploadView, ManageSendEmail

app_name = 'registration'

urlpatterns = [
    path('upload_csv', CSVUploadView.as_view(), name='upload-csv'),
    path('toggle', ManageSendEmail.as_view())
]
