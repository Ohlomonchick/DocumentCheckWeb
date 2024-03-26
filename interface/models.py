from django.db import models


class Verdict(models.Model):
    name = models.TextField(null=True)


class Message(models.Model):
    message = models.TextField()
    position = models.TextField()
    standard = models.CharField(max_length=255)
    verdict = models.ForeignKey("Verdict", on_delete=models.CASCADE)
    message_type = models.IntegerField(null=True)


