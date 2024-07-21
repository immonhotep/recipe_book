from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tinymce.models import HTMLField


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True,upload_to='images/user_images/',default='images/default_user.jpg')

    profile_bio = models.CharField(max_length=200, blank=True,null=True)
    facebook_link = models.CharField(max_length=100, blank=True,null=True)
    youtube_chanel = models.CharField(max_length=100, blank=True,null=True)

    def __str__(self):

        return self.user.username
    
    
    #if default image and uploaded image both not exist
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
def create_profile(sender,instance,created,**kwargs):
     
     if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile,sender=User)
    
    
class Food_Category(models.Model):

    name = models.CharField(max_length=200)
    image =  models.ImageField(null=True,blank=True,upload_to='images/category_images/',default='images/default.jpg')
    description = models.TextField(max_length=250)

    class Meta:

        verbose_name_plural = "Food_Categories"

    def __str__(self):

        return self.name
    
    #if default image and uploaded image both not exist
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    




class Food_Recipe(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_category = models.ForeignKey(Food_Category,on_delete=models.CASCADE)
    image =  models.ImageField(null=True,blank=True,upload_to='images/food_images/',default='images/default.jpg')
    name = models.CharField(max_length=200,unique=True)
    description = HTMLField(blank=True,default="")
    required_time = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(User,related_name='recipe_like', blank=True)
    complexity = models.CharField(max_length=100,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.name
    
    def Countlikes(self):

        return self.like.count()
    
    #if default image and uploaded image both not exist
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url





class Comments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_recipe = models.ForeignKey(Food_Recipe, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null=True, blank=True)
    likes = models.ManyToManyField(User,related_name='comment_like', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f' {self.user} - {self.comment[:20]}'

    def CountCommentLikes(self):
        return self.likes.count()


