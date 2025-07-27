# myapp/forms.py

from django import forms
from .models import Upload, Company
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from functools import lru_cache


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CompanySearchForm(forms.Form):
    keyword = forms.CharField(max_length=255, required=False)
    industry = forms.ChoiceField(choices=[('', 'Industry')], required=False)
    year_founded = forms.ChoiceField(choices=[('', 'Year Founded')], required=False)
    city = forms.ChoiceField(choices=[('', 'City')], required=False)
    state = forms.ChoiceField(choices=[('', 'State')], required=False)
    country = forms.ChoiceField(choices=[('', 'Country')], required=False)

    @staticmethod
    @lru_cache(maxsize=1)
    def get_choices(field):
        try:
            values = Company.objects.values_list(field, flat=True).distinct().order_by(field)[:100]
            return [(v, v) for v in values if v]
        except Exception:
            return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields['industry'].choices = [('', 'Industry')] + self.get_choices('industry')
            self.fields['year_founded'].choices = [('', 'Year Founded')] + self.get_choices('year_founded')
            self.fields['city'].choices = [('', 'City')] + self.get_choices('city')
            self.fields['state'].choices = [('', 'State')] + self.get_choices('state')
            self.fields['country'].choices = [('', 'Country')] + self.get_choices('country')
        except Exception:
            pass
