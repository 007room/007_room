from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from hitcount.models import HitCountMixin
from django.contrib.auth.models import AbstractUser
#from array_field_select.fields import ArrayField
Location_list =(
        ('서울특별시','서울특별시'),
        ('부산광역시','부산광역시'),
        ('세종특별시','세종특별시'),
        ('충청북도','충청북도'),
        ('충청남도','충청남도'),
        ('전라북도','전라북도'),
        ('전라남도','전라남도'),
        ('대구광역시','대구광역시'),
        ('제주특별시','제주특별시'),
        ('경상북도','경상북도'),
        ('경상남도','경상남도'),     
    )
def default_city(): # user가 회원가입할 때 지정한? 도시 or seoul
    return "seoul"

class CustomUser(AbstractUser):
    '''django 기존 User모델과 연동'''
    # REQUIRED_FIELDS = ('user',)
    # user = models.OneToOneField(User,unique=True, on_delete=models.CASCADE)
    Gender_list =(
        ('여자','여자'),
        ('남자','남자'),
        ('사용자지정','사용자지정'),
    )
    email = models.EmailField()                       
    nickname = models.CharField(max_length=10)        
    area = models.CharField(choices=Location_list, max_length=50, blank=True)
    report_count = models.IntegerField(default=0)             #신고횟수
    podo = models.IntegerField(default=10)             # 초기10알
    gender = models.CharField(choices=Gender_list, max_length=50,default=False, blank=True)    
    profile_image = models.FileField(null=True, blank=True)
    #keywords = models.CharField()                      #보류

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        
    def __str__(self):
        return "{}".format(self.email)

class Post(models.Model,HitCountMixin):
    
    Category_list = (  
        ('study','StudyRoom'), 
        ('performance','PerformanceRoom'),
        ('practice','PracticeRoom'),
        ('etc','etc'),
    )
    
    Option_list =(
        ('vim','vim'),
        ('board', 'board'),
        ('desk', 'desk'),
        ('multitap','multitap'),
        ('speaker','speaker'),
        ('lights','lights'),
        ('mirror','mirror'),
        ('air','airconditioner'),
        ('printer','printer'),
    )

        
    title = models.CharField(max_length=50)
    context = models.TextField()
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    #시간
    start_datetime = models.DateTimeField() #!!!!!!! 일정 기간을 저장하는 필드를 만들기    
    end_datetime = models.DateTimeField() 
    '''공간 유형 선택'''
    category = MultiSelectField(choices=Category_list, max_length=50, blank=True)
    etc_what = models.CharField(max_length=50, null=True,blank=True)
    price = models.IntegerField()
    '''물건 대여 선택'''
    Option = MultiSelectField(choices=Option_list, max_length=50,default=False, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)  # 글 작성 시간 :  시간이 있는 날짜를 저장하는 datetime 필드를 만들기 
    Modified_date = models.DateTimeField(auto_now=True) # 글 게시 날짜 
    rental_person = models.IntegerField(default = 1)

    def __str__(self):
        return "RoomShare : {}".format(self.title)
    
    def ROOM_TYPE(self):
        if self.category=='etc' :

            return "ROOM etc :{}".format(self.etc_what) 

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)

class Review(models.Model):
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name = 'reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirm = models.BooleanField(default=False)
    text = models.TextField(null=True)

    def __str__(self):
        return "{}".format(self.text)


class Qna(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    

    def __str__(self):
        return "{}".format(self.text)


class Application(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    #host = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    guest = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    start_date = models.IntegerField(default=1)
    end_date = models.IntegerField(default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpost = models.CharField(max_length=200)
    add_more = models.CharField(max_length=200)         # 한 마디 추가 글
    phone = models.IntegerField()
    rental_person = models.IntegerField()
    confirm = models.BooleanField(default = False)

#upload_to="anony_Board/%Y/%m/%d"
class Qna_image(models.Model):
    images = models.ImageField(blank=True,upload_to="image/qna_image/%Y/%m/%d") 
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    qna = models.ForeignKey(Qna, default=None, on_delete=models.CASCADE)


class Post_image(models.Model):
    images = models.ImageField(blank=True,upload_to="image/post_image/%Y/%m/%d") 
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)


class Review_image(models.Model):
    images = models.ImageField(blank=True,upload_to="image/review_image/%Y/%m/%d") 
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, default=None, on_delete=models.CASCADE)


class Date(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    start_date = models.IntegerField(default=1)
    end_date = models.IntegerField(default=1)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)


class Post_like(Like):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE, related_name = 'post_likes')


class Review_like(Like):
    review = models.ForeignKey(Review, default=None, on_delete=models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    qna = models.ForeignKey(Qna, default=None, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "{}".format(self.text)


class Report(models.Model):
    reporter_user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)
    reported_user = models.CharField(max_length=200)
    reason = models.TextField()
    image = models.FileField(null=True, blank=True)
    post_url = models.CharField(max_length=500)

class Podo(models.Model):
    podo = models.IntegerField() # +3 | -2
    reason = models.CharField(max_length=20) #빌릴때 - | 충전 + | 후기컨펌받으면 +  

    # def save(self, *args, **kwargs):
    #     if a == review_confirm
    #     reason = '후기컨펌받음'