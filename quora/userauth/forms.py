from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from userauth.models import Gender, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'gender', 'image']


class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-control form-control-lg'}), max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-control form-control-lg'}), max_length=50)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control form-control-lg'}), max_length=50)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
                             'placeholder': 'Age', 'class': 'form-control form-control-lg'}),)
    gender = forms.ChoiceField(choices=Gender.choices, widget=forms.Select(
        attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control form-control-lg'}))

    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name',
                  'last_name', 'age', 'gender', 'image']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, user=None):
        profile = super(UserProfileForm, self).save(commit=False)

        if user:
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()

            profile.user = user

        profile.save()
        return profile


class UserSignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control form-control-lg'}), max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'form-control form-control-lg'}))
    
    class Meta:
        fields = ['username', 'password']


class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-control form-control-lg'}), max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-control form-control-lg'}), max_length=50, required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control form-control-lg'}), max_length=50, required=True)
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
                             'placeholder': 'Age', 'class': 'form-control form-control-lg'}), required=True)
    gender = forms.ChoiceField(choices=Gender.choices, widget=forms.Select(
        attrs={'class': 'form-control form-control-lg'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'form-control form-control-lg'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
