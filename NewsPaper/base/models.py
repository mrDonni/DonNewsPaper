from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posted = Post.objects.filter(author = self)
        post_ratings = sum(i.rating for i in posted)
        comment_ratings = sum(i.rating for i in Comment.objects.filter(user = self.user))
        postcomment_ratings = 0
        for j in posted:
            for i in Comment.objects.filter(post=j):
                postcomment_ratings += i.rating
        self.rating = (3 * post_ratings) + comment_ratings + postcomment_ratings
        self.save()
        return self.rating



class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):

    article = 'AR'
    post = 'PS'
    TYPES =[
        (article, 'Новость'),
        (post, 'Статья')
    ]

    type = models.CharField(max_length= 2,
                            choices= TYPES,
                            default= article)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through= 'PostCategory')
    name = models.CharField(max_length= 255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating +1
        self.save()
        return self.rating


    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        preview = str(self.text)[:124].replace('\n', '')
        return preview

    def __str__(self):
        return f"{self.name.title()}:{self.text[:20]}"

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text= models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating +1
        self.save()
        return self.rating

    def dislike(self):
        self.rating = self.rating -1
        self.save()
        return self.rating



