from django.urls import path

from interface.views import *

urlpatterns = [
    path("", upload_file, name="home")
]