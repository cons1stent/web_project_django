from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#
#
# class UserForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#
#     class Meta:
#             model = User
#             fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
#
#
# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = Profile
#         fields = ['birthdate', 'phonenumber']
#         widgets = {
#             'birthdate': DateInput(attrs={'type': 'date'}),
#         }
#
# class NewUserForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
