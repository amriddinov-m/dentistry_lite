import re

from django import forms

from user.models import User


class LoginForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        formatted_number = '+' + re.sub(r'\D', '', phone.lstrip('+'))
        return formatted_number


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'password', 'role', 'fullname', 'address', 'birthday', 'start_time', 'end_time', 'status')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        formatted_phone = '+' + re.sub(r'\D', '', phone.lstrip('+'))
        return formatted_phone

    def save(self, commit=True):
        self.cleaned_data['phone'] = self.clean_phone()
        return super().save(commit=commit)
