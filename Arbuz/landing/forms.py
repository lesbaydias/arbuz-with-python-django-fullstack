# import django_filters
from django import forms
from django.contrib.auth.models import User

from landing.models import ItemTable, Payment_Card


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemTable
        fields = [
            "name",
            "category",
            "image_field",
            "price",
            "country",
        ]




class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
    email = forms.EmailField(required=False)
    username = forms.CharField(label='Username', max_length=100, required=False)
    first_name = forms.CharField(label='First name',required=False)
    last_name = forms.CharField(label='Last name', required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required.')
        return last_name


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already taken.')
        if not username:
            raise forms.ValidationError('Username is required.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError('Both password fields are required.')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Username is required.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')

        if not password:
            raise forms.ValidationError('Password fields is required.')

        return cleaned_data


class Edit(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]
    email = forms.EmailField(required=False)
    first_name = forms.CharField(label='First name',required=False)
    last_name = forms.CharField(label='Last name', required=False)
    username = forms.CharField(label='Username', max_length=100, required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required.')
        return last_name


    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('Username is required.')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError('Both password fields are required.')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class contactformemail(forms.Form):
    fromemail = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class Payment(forms.ModelForm):
    class Meta:
        model = Payment_Card
        fields = [
            "cardholder_name",
            "card_number",
            "expiration_year",
            "expiration_month",
            "balance",
            "cvv",
        ]

    cardholder_name = forms.CharField(label='Cardholder name: ', max_length=100)
    card_number = forms.CharField(label='Card number:', max_length=16)
    expiration_year = forms.IntegerField(label="Expiration year: ")
    expiration_month = forms.IntegerField(label="Expiration month")
    balance = forms.IntegerField()
    cvv = forms.CharField(label='CVV', max_length=4)


class EditPayment(forms.Form):
    fields = [
        "card_number",
        "balance",
    ]
    card_number = forms.CharField(label='Card number:', max_length=16)
    balance = forms.IntegerField()


class EditPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "password1",
            "password2",
        ]
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Password must contain at least one digit.')
        if not any(char.islower() for char in password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise forms.ValidationError('Both password fields are required.')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
        ]
    email = forms.EmailField(required=False)
    first_name = forms.CharField(label='First name',required=False)
    last_name = forms.CharField(label='Last name', required=False)
    username = forms.CharField(label='Username', max_length=100, required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('Email is required.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('First name is required.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('Last name is required.')
        return last_name


    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError('Username is required.')
        return username