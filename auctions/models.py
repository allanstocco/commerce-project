from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE
from django.db.models.deletion import PROTECT
from django.db.models.fields import NullBooleanField
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import related



CATEGORY = (
    ("HOME", "Home & Garden"),
    ("BOOKS", "Books"),
    ("TECH", "Eletronic & Computers"),
    ("ENTERTAIN", "Films, Music & Games"),
    ("BEAUTY", "Health & Beauty"),
    ("FASHION", "Clothes, Shoes, Jewellery and Accessories"),
    ("BABY", "Toys, Children & Baby"),
    ("SPORTS", "Sports & Outdoors"),
    ("MOTORS", "Car & Motorbike"),
    ("OTHER", "Other")
)



class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    products = models.ForeignKey('Products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'price'

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    field = models.CharField(max_length=2048)
    products = models.ForeignKey('Products', on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)


class Products(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1024, null=True, blank=True)
    pictureURL = models.CharField(max_length=2048, null=True, blank=True)
    pictureUpload = models.FileField(upload_to='images', null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.CharField(max_length=20, blank=True, choices=CATEGORY, default="OTHER")
    higherBid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="higherBid", null=True, blank=True)
    status = models.BooleanField(default=True)
    user_seller = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    bid_timer = models.DateTimeField(null=True, blank=True)
    
    @property
    def get_picture_upload(self):
        if self.pictureUpload and hasattr(self.pictureUpload, 'url'):
            return self.pictureUpload.url
