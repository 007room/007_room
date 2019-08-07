from django.contrib import admin
from .models import CustomUser, Post, Review, Qna, Application, Qna_image, Post_image, Date, Post_like, Review_like, Comment, Review_image
# Register your models here.

admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Qna)
admin.site.register(Application)
admin.site.register(Qna_image)
admin.site.register(Post_image)
admin.site.register(Date)
admin.site.register(Post_like)
admin.site.register(Review_like)
admin.site.register(Comment)
admin.site.register(CustomUser)
admin.site.register(Review_image)


