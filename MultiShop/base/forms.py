# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'father_name', 'username', 'email', 'password', 'gender', 'province', 'city', 'dob', 'phone', 'about', 'profile_pic']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Check if the username is an email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = None
        else:
            user = User.objects.get(username=username)
        if user is not None:
            # Authenticate the user with provided password
            if user.check_password(password):
                self.user_cache = user
            else:
                raise forms.ValidationError("Invalid email or password.")
        else:
            raise forms.ValidationError("Invalid email or password.")

        return self.cleaned_data
    


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'father_name', 'username', 'email', 'gender', 'province', 'city', 'dob', 'phone', 'about', 'profile_pic']

