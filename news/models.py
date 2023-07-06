from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    userModel = models.OneToOneField(User, on_delete=models.CASCADE)
    userRate = models.IntegerField(default = 0)

    def update_rating(self):
        self.userRate = 0
        #суммарный рейтинг каждой статьи автора умножается на 3
        authPosts = Post.objects.filter(postAuthor__id = self.id).values('postRate')
        for post in authPosts:
            self.userRate += post['postRate'] * 3
        
        #суммарный рейтинг всех комментариев автора
        authComments = Comment.objects.filter(fromUser__id = self.userModel.id).values('commentRate')
        for post in authComments:
            self.userRate += post['commentRate'] 

        #суммарный рейтинг всех комментариев к статьям автора
        authPostComments = Comment.objects.filter(toPost__postAuthor__id = self.id).values('commentRate')
        for post in authPostComments:
            self.userRate += post['commentRate'] 

        self.save()


class Category(models.Model):
    categoryName = models.CharField(max_length = 255, unique = True)

class Post(models.Model):
    news = 'N'
    article = 'A'
    postChoice = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    postAuthor = models.ForeignKey(Author, on_delete = models.CASCADE)
    postType = models.CharField(max_length = 1, choices = postChoice, default = news)
    postDateTime = models.DateTimeField(auto_now_add = True)
    postCat = models.ManyToManyField(Category, through = 'PostCategory')
    postTitle = models.CharField(max_length = 255, default = 'Заголовок')
    postBody = models.TextField(default = 'Здесь должен быть текст')
    postRate = models.IntegerField(default = 0)

    def like(self):
        self.postRate += 1
        self.save()
    
    def dislike(self):
        self.postRate -= 1
        self.save()
    
    def preview(self, count=124):
        if (len(self.postBody) <= count):
            return self.postBody
        else:
            return self.postBody[:count-3]+'...'
        
    


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    toPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    fromUser = models.ForeignKey(User, on_delete = models.CASCADE)
    commentDateTime = models.DateTimeField(auto_now_add = True)
    commentBody = models.TextField(default = 'Комментарий')
    commentRate = models.IntegerField(default = 0)

    def like(self):
        self.commentRate += 1
        self.save()
    
    def dislike(self):
        self.commentRate -= 1
        self.save()


