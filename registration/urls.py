from django.urls import path
from .views import CSVUploadView, ManageSendEmail, RegistrationStatus

app_name = 'registration'

urlpatterns = [
    path('upload_csv', CSVUploadView.as_view(), name='upload-csv'),
    path('toggle', ManageSendEmail.as_view()),
    path('data_status', RegistrationStatus.as_view()),
]
