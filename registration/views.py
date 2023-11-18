import json
import threading
from concurrent.futures import ThreadPoolExecutor
import csv
import chardet
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CSVUploadSerializer
from .models import EmailStatus, UserDataStatus
from .utils import send_email_background, process_row, insert_data


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):

        serializer = CSVUploadSerializer(data=request.data)

        if serializer.is_valid():
                csv_file = serializer.validated_data['csv_file']

                raw_content = csv_file.read()
                encoding_result = chardet.detect(raw_content)
                detected_encoding = encoding_result['encoding']

                content = raw_content.decode(detected_encoding)
                rows = csv.reader(content.splitlines())

                thread = threading.Thread(target=insert_data, args=(rows,))
                thread.start()

                return Response({'message': 'CSV file upload started successfully.'},
                                        status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManageSendEmail(APIView):
    def post(self, request):

        email_status = EmailStatus.objects.get(id=1)

        email_status.is_sending = not email_status.is_sending
        email_status.save(update_fields=["is_sending"])

        thread = threading.Thread(target=send_email_background, args=(email_status,))
        thread.start()

        return JsonResponse({'status': 'success', "paused": email_status.is_sending})

    def get(self, request):
        email_status = EmailStatus.objects.get(id=1)
        return JsonResponse({'total_emails': email_status.total_emails, 'emails_sent': email_status.emails_sent, 'is_sending': email_status.is_sending})


class RegistrationStatus(APIView):

    def get(self, request):
        data_status = UserDataStatus.objects.all().last()
        if data_status.errors:
            errors = json.loads(data_status.errors)
        else:
            errors = []
        return Response({"done": data_status.inserted, "errors": errors})
