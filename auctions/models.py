from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing')

class Listing(models.Model):
    title = models.CharField(max_length=150)
    description =models.TextField()
    price = models.IntegerField()
    image_url = models.URLField(max_length = 200)
    category = models.CharField(max_length=100)
    seller =  models.ForeignKey(User, on_delete = models.CASCADE, related_name='mylisting')
    time_posted = models.DateTimeField(default=datetime.now())
    status= models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="offer")
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bidder} {self.amount}"

class Comment_on_listing(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mycomment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    comment_text= models.TextField()

    def __str__(self):
        return f"{self.commenter} {self.comment_text}"

