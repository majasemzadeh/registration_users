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
from .models import EmailStatus
from .utils import send_email_background, process_row


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

                with transaction.atomic():
                    with ThreadPoolExecutor() as executor:
                        errors = list(executor.map(process_row, rows))

                    error_messages = [error for error in errors if error]
                    if error_messages:

                        return Response({'errors': error_messages}, status=status.HTTP_400_BAD_REQUEST)
                    else:

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

