from django import forms
from django.contrib.auth.models import User
from .models import Service,Subscription,login

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = login
        fields = ['username', 'email', 'password']




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'payment_terms', 'price', 'package', 'tax', 'image', 'active']



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['user','service','amount']

    def __init__(self,*args,**kwargs):
        super(SubscriptionForm,self).__init__(*args,**kwargs)
        self.fields['service'].queryset = Service.objects.filter(active = True)


class signin(forms.ModelForm):
    class Meta:
        model=login
        fields=('username','password')
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = login.objects.get(username=username)
                if user.password != password:
                    raise forms.ValidationError('incorrect username or password')
            except login.DoesNotExist:
                raise forms.ValidationError('incorrect username or password')
        return cleaned_data