# myapp/forms.py

from django import forms
from .models import Upload, Company
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
    industry = forms.ChoiceField(choices=[('', 'Industry')] + [(industry, industry) for industry in Company.objects.values_list('industry', flat=True).distinct().order_by('industry')], required=False)
    year_founded = forms.ChoiceField(choices=[('', 'Year Founded')] + [(year_founded, year_founded) for year_founded in Company.objects.values_list('year_founded', flat=True).distinct().order_by('year_founded')], required=False)
    city = forms.ChoiceField(choices=[('', 'City')] + [(city, city) for city in Company.objects.values_list('city', flat=True).distinct().order_by('city')], required=False)
    state = forms.ChoiceField(choices=[('', 'State')] + [(state, state) for state in Company.objects.values_list('state', flat=True).distinct().order_by('state')], required=False)
    country = forms.ChoiceField(choices=[('', 'Country')] + [(country, country) for country in Company.objects.values_list('country', flat=True).distinct().order_by('country')], required=False)
