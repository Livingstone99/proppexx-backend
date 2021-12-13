from users.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
# Create your models here.

class Article(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length= 100, unique= True)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    slug = models.SlugField(editable= False)
    images = models.URLField()
    tag =ArrayField(
        models.CharField(max_length=20, blank=True, null=True),blank = True, null = True, size = 10
    )
    # display = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.writer} wrote {self.slug}'
    



