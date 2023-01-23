from django.shortcuts import render
from rest_framework import generics, status, permissions
from django.http import JsonResponse, HttpResponse
import traceback

from .serializers import *
from .models import *

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


class UserSignup(generics.GenericAPIView):
    def post(self, request):
        permissions_class = (permissions.AllowAny, )
        userdata = request.data
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            subject = "["+serializer.data['name']+"]의 회원가입 인증 메일입니다."
            to = ["signup.cardmanager@gmail.com"]
            message = render_to_string('templates/signup.html', context={'url' : url})
            return JsonResponse({'message' : 'Success'}, status=status.HTTP_200_OK)
        return JsonResponse({'message' : 'Fail'}, status=status.HTTP_400_BAD_REQUEST)


class UserActivate(generics.GenericAPIView):
    permissions_class = (permissions.AllowAny, )

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64.encode('utf-8')))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponse(user.email + '계정이 활성화 되었습니다', status=status.HTTP_200_OK)
            else:
                return HttpResponse('만료된 링크입니다', status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(traceback.format_exc())
