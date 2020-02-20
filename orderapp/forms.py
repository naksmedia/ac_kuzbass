from django import forms
# from django.core.validators import FileExtensionValidator, validate_email
from captcha.fields import CaptchaField
from .models import OrderService
import os


class OrderForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = OrderService
        fields = ['name', 'phone', 'email', 'compound']
        widgets = {
                'name': forms.TextInput({
                'placeholder': "Ваше имя",
                'class': 'form-control form-control-sm',
                }),
                'phone': forms.TextInput({
                    'placeholder': 'Ваш телефон',
                    'class': 'form-control form-control-sm',
                    'type': 'text',
                }),
                'email': forms.TextInput({
                    'placeholder': 'Ваш email',
                    'class': 'form-control form-control-sm',
                    'type': 'text',
                }),
                # <input type="text" class="form-control form-control-sm" placeholder=""  type="text" id="phone2" required="">
            }