from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating = 3 * (int(Post.objects.filter(author = self).values('rating'))) + Comment.objects.filter(user = self.user).values('rating')
        #self.Comment.rating + self.Post.Comment.rating +
        return self.rating

class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)

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
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length= 255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating +1
        return self.rating

    def dislike(self):
        self.rating -= 1
        return self.rating

    def preview(self):
        preview = str(self.text)[:124].replace('\n', '')
        return preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text= models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating +1
        return self.rating

    def dislike(self):
        self.rating = self.rating -1
        return self.rating



