from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import data_serializer
from .models import vitals_data
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.settings import api_settings
renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# Create your views here.


@api_view(['GET'])
def get(request):
    # data = vitals_data.objects.all()
    data = vitals_data.objects.get(id=6)
    serialize = data_serializer(data)
    return Response(serialize.data)


@api_view(['POST','GET'])
def post(request):
    # data = JSONParser().parse(request)
    # print(courseSerializer)

    # data_p = {
    #     "temperature": 90.0,
    #     "temperature_flag": 2,
    #     "systolic_bp": 100,
    #     "systolic_bp_flag": 2,
    #     "diastolic_bp": 50,
    #     "diastolic_bp_flag": 2,
    #     "pulse_rate": 80,
    #     "pulse_rate_flag": 2,
    #     "oxygen_saturation": 98,
    #     "oxygen_saturation_flag": 2
    # }
    data_ser = data_serializer(data=request.data)
    if data_ser.is_valid():
        data_ser.save()
        return Response(data_ser.data, status=status.HTTP_201_CREATED)

    return Response(data_ser.errors)


@api_view(['PUT','GET'])
def put(request,ids):
    try:
        data = vitals_data.objects.get(id=ids)
    except:
        print("Not found")

    # if request.method=='PUT':
        # serializer= data_serializer(data)
        # data_p= {
        #     "temperature": 100.0,
        #     "temperature_flag": 2,
        #     "systolic_bp": 100,
        #     "systolic_bp_flag": 2,
        #     "diastolic_bp": 50,
        #     "diastolic_bp_flag": 2,
        #     "pulse_rate": 80,
        #     "pulse_rate_flag": 2,
        #     "oxygen_saturation": 98,
        #     "oxygen_saturation_flag": 2
        # }

    serializer= data_serializer(data,request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response(status=status.HTTP_200_OK)
    # print(courseSerializer)
    # data_ser = data_serializer(data=data)
    # if data_ser.is_valid():
    #     data_ser.save()
    #     return Response(data_ser.data, status=status.HTTP_201_CREATED)

    # return Response(data_ser.errors)
