from django import forms


class link(forms.Form):
    linkget=forms.CharField(label='link' ,max_length=200)