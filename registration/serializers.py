from rest_framework import serializers


class CSVUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()