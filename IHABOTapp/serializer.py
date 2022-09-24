from rest_framework import serializers
from .models import vitals_data


class data_serializer(serializers.ModelSerializer):

    class Meta:
        model = vitals_data
        fields = '__all__'
