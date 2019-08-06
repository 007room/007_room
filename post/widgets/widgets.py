'''custom form에서 사용될 widget을 위한 class 정의하는 곳'''
from main.models import Post, Review, Qna, Review_image
from .forms import ReviewForm, QnaForm, ImageFormSet,PostForm,DateInput,MultipleChiceField,OptionForm

class TagsInputWidget(forms.SelectMultiple):
    def render(self, name, value, attrs):
        context = {
            'select_options' = [ item for item in self.choices ]
            'name' = name
        }

        html = render_to_string('widgets/tagsinput.html', context)

        return html



