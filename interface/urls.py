from django.urls import path

from interface.views import *

urlpatterns = [
    path('<int:pk>', upload_file, name='result'),
    path("", upload_file, name="home")
]