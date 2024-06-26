from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UploadFileForm
from docsCheck.runners import run_check
from docsCheck.utils import MessageTypes
from django.contrib import messages as global_messages
import time
import os
from interface.models import *


def handle_uploaded_file(file, category: str):
    doc_path = os.path.join(settings.MEDIA_ROOT, file._name)
    with open(doc_path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    verdict = run_check(doc_path, doc_type=category)
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
    context = {}

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            category = request.POST.get('doc_type', None)
            try:
                pk = handle_uploaded_file(request.FILES["file"], category)
                return redirect(f"/{pk}")
            except RuntimeError:
                form.add_error("file", "Ошибка во время анализа. Возможно, файл повреждён.")
        context = {"form": form}
    else:
        form = UploadFileForm()
        context = {"form": form}
        if pk is not None:
            verdict = get_object_or_404(Verdict, id=pk)
            messages = Message.objects.filter(verdict=verdict)
            context["messages"] = messages

    return render(request, "index.html", context=context)
