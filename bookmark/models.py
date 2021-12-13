from django.db import models
from users.models import User
from property.models import Property, Feature

# Create your models here.

class BookmarkProperty(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['buyer', 'property']
        verbose_name_plural = "bookmark Properties"
        # get_latest_by = "created_at"

class BookmarkFeature(models.Model):
    """this works like bookmarking tags"""
    buyer = models.OneToOneField(User, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.buyer