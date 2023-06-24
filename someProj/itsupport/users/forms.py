from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Problem,Comment
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['problem_description', 'problem_type', 'floor', 'room_number']
        widgets = {
            'problem_description': forms.Textarea(attrs={'class': 'form-control'}),
            'problem_type': forms.Select(attrs={'class': 'form-select'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'room_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReportForm(forms.Form):
    STATUS_CHOICES = (
        ('resolved', 'Resolved'),
        ('in_progress', 'In Progress'),
        ('not_resolved', 'Not Resolved'),
    )

    solution = forms.CharField(label='Solution', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect)
    notes = forms.CharField(label='Notes', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))