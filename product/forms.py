from django  import forms


class SearchForm(forms.Form):
    search_bar = forms.CharField(max_length=256)
