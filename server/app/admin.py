from app.models import Credentials
from data.providers import PROVIDERS
from data.core import LoginError

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class UserCreateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(get_random_string())
        if commit:
            user.save()
        return user


class UserAdmin(UserAdmin):
    add_form = UserCreateForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',)
        }),
    )


class CredentialsForm(forms.ModelForm):

    email = forms.EmailField(label='Email authorized by the customer')
    setup_link = forms.CharField(label='Setup link received in mail')

    class Meta:
        model = Credentials
        fields = ('owner', 'provider')


    def clean_provider(self):
        provider = self.cleaned_data["provider"].lower()
        if provider not in PROVIDERS:
            raise forms.ValidationError("Unknown provider")
        return provider

    def clean_setup_link(self):
        if "provider" not in self.cleaned_data:
            return self.cleaned_data['setup_link']
    
        provider = PROVIDERS[self.cleaned_data["provider"].lower()]
        api = provider.api(self.cleaned_data["owner"])
        try:
            api.set_credentials(self.cleaned_data['email'], self.cleaned_data['setup_link'])
        except LoginError:
            raise forms.ValidationError("There is an issue with the mail or the link")
        return self.cleaned_data['setup_link']

    def save(self, commit=False):
        credentials = super().save(commit=False)
        return credentials

    

class CredentialsAdmin(admin.ModelAdmin):
    form = CredentialsForm


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Credentials, CredentialsAdmin)