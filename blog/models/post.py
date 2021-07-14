from django.db import models


class DateTimePicker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    c_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.c_name

class Tutorial(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name="tutorials")

    def __str__(self):
        return self.name
    

class Post(DateTimePicker):
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="posts",blank=True,null=True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name="posts")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="posts")
    likes = models.ManyToManyField('auth.User',blank=True,related_name="likes")
    views = models.ManyToManyField('auth.User',blank=True,related_name="views")
    tutorial = models.ForeignKey(Tutorial,on_delete=models.CASCADE,related_name="posts",null=True)

    def __str__(self):
        return self.title
    



class Comment(DateTimePicker):
    content = models.TextField()
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name="comments")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    def __str__(self):
        return self.post

class Reply(DateTimePicker):
    content = models.TextField()
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,related_name="replies")
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="replies")
