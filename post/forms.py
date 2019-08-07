from django import forms

from main.models import Post, Review, Qna, Review_image

 
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
    # images = forms.ImageField( widget=forms.FileInput)
    class Meta:
        model = Review_image
        fields = ['images',]

# ImageFormSet = forms.inlineformset_factory(Review, Review_image, form=ImageForm, extra=2)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','category','etc_what','Option','choose_date','context')
    