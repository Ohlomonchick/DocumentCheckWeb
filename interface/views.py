from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UploadFileForm
from docsCheck.runners import run_check
from docsCheck.utils import MessageTypes
import time
import os
from interface.models import *


def handle_uploaded_file(file):
    doc_path = os.path.join(settings.MEDIA_ROOT, file._name)
    with open(doc_path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    verdict = run_check(doc_path)
    verdict_db = Verdict.objects.create(name=file._name)
    messages_db = []
    for message in verdict.messages:
        t = 0
        if message.message_type == MessageTypes.WARNING:
            t = 1
        message_db = Message(
            message=message.text,
            standard=message.standard,
            message_type=t,
            position=message.position,
            verdict=verdict_db
        )
        messages_db.append(message_db)

    Message.objects.bulk_create(messages_db)
    return verdict_db.id


def upload_file(request, pk=None):
    if request.method == "POST":
        print("lalala")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pk = handle_uploaded_file(request.FILES["file"])
            return redirect(f"/{pk}")
    else:
        form = UploadFileForm()
        context = {"form": form}
        if pk is not None:
            verdict = get_object_or_404(Verdict, id=pk)
            messages = Message.objects.filter(verdict=verdict)
            context["messages"] = messages

    return render(request, "index.html", context=context)