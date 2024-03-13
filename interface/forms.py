from django import forms
from django.core.exceptions import ValidationError

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        # Get the uploaded file
        uploaded_file = self.cleaned_data.get('file')
        print("dddddd")
        # Check if the file has an extension and if it's .docx
        if uploaded_file:
            extension = uploaded_file.name.split('.')[-1].lower()
            if extension != 'docx':

                raise ValidationError('Пожалуйста, загрузите .docx файл.')


        # Always return the cleaned data
        return uploaded_file