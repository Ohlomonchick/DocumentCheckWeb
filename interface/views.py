from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import time


def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == "POST":
        print("lalala")
        time.sleep(1)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/result")
    else:
        form = UploadFileForm()


    return render(request, "index.html", {"form": form})