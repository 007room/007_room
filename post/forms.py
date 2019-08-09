from main.models import *#Post, Review, Qna, Review_image, Comment, Report
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import inlineformset_factory
from django.forms.widgets import (
    FILE_INPUT_CONTRADICTION, CheckboxInput, ClearableFileInput, DateInput,
    DateTimeInput, EmailInput, HiddenInput, MultipleHiddenInput,
    NullBooleanSelect, NumberInput, Select, SelectMultiple,
    SplitDateTimeWidget, SplitHiddenDateTimeWidget, TextInput, TimeInput,
    URLInput,
)
from bootstrap_datepicker_plus import DateTimePickerInput

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
        fields = ('text',)

class CommentForm(ReviewForm):
    class Meta:
        model = Comment
        fields = ('text',)
    

# class PostImageForm(forms.ModelForm):
#     post_pk = forms.IntegerField(widget=forms.HiddenInput)
#     # images = forms.ImageField( widget=forms.FileInput)
#     class Meta:
#         model = Post_image
#         fields = ['images',]

class ImageForm(forms.ModelForm):
    review_pk = forms.IntegerField(widget=forms.HiddenInput)
    # images = forms.ImageField( widget=forms.FileInput)
    class Meta:
        model = Review_image
        fields = ['images',]

class ConfirmForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['confirm',]

ImageFormSet = forms.inlineformset_factory(Review, Review_image, form=ImageForm, extra=2)
# PostImageFormSet = forms.inlineformset_factory(Post, Post_image, form=ImageForm, extra=2)
        
     
'''custom field class widget 설정 및 유효성 검사 메소드 정의 '''
# class MultipleChiceField(forms.ModelMultipleChoiceField):  # multipleChiceField 상속함
#     widget = TagsInputWidget # widgets.py에서 정의 
    
#     def _check_values(self,value):
#         return value[0].split(',')

# class OptionForm(ModelForm): # MultipleChoicField에서 사용할 필드를 지정하기 
#     options = MultipleChiceField(queryset=Post.Option.all())
#     categories = MultipleChiceField(queryset=Post.category.all())


class MyDatePickerInput(DateTimePickerInput):
    template = 'post/datetimepicker.html'

class PostForm(forms.ModelForm):
    post_pk = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Post
        fields = ('title','category','etc_what','start_datetime','end_datetime','Option','price','context',)
       
        widgets = {
            'start_datetime':MyDatePickerInput(options={'debug': True}),
            'end_datetime':MyDatePickerInput(options={'debug': True}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', '글 올리기'))



class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('reported_user', 'reason', 'post_url', 'image')
   
