from django import forms


class NewPost(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
