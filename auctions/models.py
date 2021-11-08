from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    choice = [
        ('Fashion', 'Fashion'),
        ('Toy', 'Toy'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        ('Travel', 'Travel'),
        ('other', 'other'),
    ]
    title = models.CharField(max_length=64)
    description = models.TextField()
    base_price = models.FloatField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=30, choices=choice)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item_owner")
    open = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.id}: {self.title} for {self.base_price} $"


class Bid(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participated_bid")
    price = models.FloatField()

    def __str__(self):
        return f"{self.user_id} bids on item:{self.listing_id} with price ${self.price}"


class Comment(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_comment")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user_id} comments on {self.listing_id}: {self.comment}"
