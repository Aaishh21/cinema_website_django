from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'login_form', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login_form', 'placeholder': 'Enter your password'}))

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'field', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={    
        'class': 'field', 'placeholder': 'Enter your email address'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'field', 'placeholder': 'Enter your phone number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email_prefix = self.cleaned_data['email'].split('@')[0]
        username = email_prefix
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{email_prefix}{counter}"
            counter += 1
        user.username = username
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'field', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={    
        'class': 'field', 'placeholder': 'Enter your email address'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'field', 'placeholder': 'Enter your phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'field', 'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('image', 'full_name', 'email', 'phone_number', 'password')