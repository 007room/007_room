from django import forms

from .models import Post, Review, Qna, Review_image


class ReviewForm(forms.ModelForm):
    post_pk = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Review
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['text'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "This is a placeholder test",
            'rows': 10
        }

class QnaForm(ReviewForm):
    class Meta:
        model = Qna
        fields = ('context',)
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['context'].widget.attrs = {
            'class': 'form-control',
            'placeholder': "This is a placeholder test",
            'rows': 10
        }


class ImageForm(forms.ModelForm):
    review_pk = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = Review_image
        fields = ['images',]

ImageFormSet = forms.inlineformset_factory(Review, Review_image, form=ImageForm, extra=2)
        
    
    
#원래 (forms) 인데 오류나서 고쳐봄
class SearchForm(forms.Form):
    word = forms.CharField(label='Search Word')
