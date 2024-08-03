from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import customuser,Order, CustomerReview , Querries
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SignupForm(forms.ModelForm):
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    class Meta:
        model = customuser
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

        if '@' in username:
            try:
                user = customuser.objects.get(email=username)
            except customuser.DoesNotExist:
                raise ValidationError(_('Invalid email or password.'), code='invalid')
        else:
            user = customuser.objects.filter(username=username).first()

        if user is not None and user.check_password(password):
            if user.is_active:
                self.user_cache = user
            else:
                raise ValidationError(_('This account is inactive.'), code='inactive')
        else:
            raise ValidationError(_('Invalid email or password.'), code='invalid')

        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = customuser
        fields = ['first_name', 'last_name', 'father_name', 'username', 'email', 'gender', 'province', 'city', 'dob', 'phone', 'about', 'profile_pic']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'address', 'country', 
            'city', 'state', 'zip_code', 'shipping_first_name', 'shipping_last_name', 
            'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_country', 
            'shipping_city', 'shipping_state', 'shipping_zip_code', 'payment_method', 'status'
        ]
        
        
class CustomerReviewForm(forms.ModelForm):
    class Meta:
        model = CustomerReview
        fields = ['profession', 'review', 'product']
        widgets = {
            'product': forms.HiddenInput(),
        }
        
class QuerriesForm(forms.ModelForm):
    class Meta:
        model = Querries
        fields = [
            'subject', 'message'
        ]
        
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message',
            }),
        }