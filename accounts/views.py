from django.shortcuts import render
from rest_framework import generics, status
from django.http import JsonResponse

from .serializers import *
from .models import *


class Signup(generics.GenericAPIView):
    def post(self, request):
        userdata = request.data
        serializer = SignupSerializer

        if serializer.is_valid():
            serializer.save()
            send(request, userdata['email'])
            return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)
        return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)
