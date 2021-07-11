from django.db import models



class Profile(models.Model):
    gender_choices = (
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    user = models.OneToOneField('auth.User',on_delete=models.CASCADE,related_name="profile")
    avatar = models.ImageField(upload_to="avatar/",null=True,blank=True)
    address = models.CharField(max_length=150,blank=True)
    birth_date = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=10,choices=gender_choices,default=gender_choices[0][1])

    def __str__(self):
        return self.user.username