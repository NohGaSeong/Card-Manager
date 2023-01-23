from django.urls import path
from .views import *

urlpatterns = [
    path("/signup",UserSignup.as_view(), name = "videoDetail"),
    path("/activate",UserActivate.as_view(), name = "commentAPI"),
]
