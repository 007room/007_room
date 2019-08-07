from django import forms

#원래 (forms) 인데 오류나서 고쳐봄
class SearchForm(forms.Form):
    word = forms.CharField(label='Search Word')



    