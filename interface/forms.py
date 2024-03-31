from django import forms
from django.core.exceptions import ValidationError
from docsCheck.checker import full_allowed_checkers_name


class UploadFileForm(forms.Form):
    file = forms.FileField()
    doc_type = forms.ChoiceField(
        choices=tuple([(key, value) for key, value in full_allowed_checkers_name.items()])
    )

    def clean_file(self):
        # Get the uploaded file
        uploaded_file = self.cleaned_data.get('file')
        # Check if the file has an extension and if it's .docx
        if uploaded_file:
            extension = uploaded_file.name.split('.')[-1].lower()
            if extension != 'docx':
                raise ValidationError('Пожалуйста, загрузите .docx файл.')


        # Always return the cleaned data
        return uploaded_file