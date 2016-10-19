from django import forms

from .models import Review

class ReviewForm(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    text = forms.CharField(label="text", widget=forms.Textarea,
                           max_length=10000)
