from django import forms
from django.core.exceptions import ValidationError
from news.models import Advertiser, Search
import re


class AdForm(forms.ModelForm):
    class Meta:
        model = Advertiser
        fields = ("name",
                  "phone",
                  "company_name",
                  "subject",
                  "email",
                  "text")

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone")
        if not phone or not re.match("^\+?\d{11}$", phone):
            raise ValidationError({"phone": "Неправильный номер телефона. Введите верный номер."})

        name = cleaned_data.get("name")
        if not name or len(name) < 2:
            raise ValidationError({"name": "Ваше ФИО слишком короткое. Введите верное ФИО."})

        text = cleaned_data.get("text")
        if not text or len(text) < 5:
            raise ValidationError({"text": "Текст сообщения слишком короткий. Введите текст сообщения."})

        subject = cleaned_data.get("subject")
        if not subject:
            raise ValidationError({"subject": "Введите тему сообщения."})

        email = cleaned_data.get("email")
        if not email:
            raise ValidationError({"email": "Введите верный email."})

        return cleaned_data


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ("search",)

    def clean(self):
        cleaned_data = super().clean()

        search = cleaned_data.get("search")
        if not search:
            raise ValidationError({"search": "Вы не ввели слово для поиска."})
