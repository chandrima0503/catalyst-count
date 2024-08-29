from rest_framework import serializers

class RecordCountSerializer(serializers.Serializer):
    count = serializers.IntegerField()