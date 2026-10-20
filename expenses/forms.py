from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Category,Income,Expense


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

class editProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'bio', 'profile_img', 'location', 'social_linkedin', 'social_instagram', 'social_twitter']

class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class addIncomeForm(forms.ModelForm):
    class Meta:
        model=Income
        fields=['source','amount','date']
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Enter amount (no commas)'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
class addExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','category','date','description']
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'Enter amount (no commas)'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

