from django.db import models
from users.models import User

# Create your models here.
Categories = (
    ('rent', 'Rent'),
    ('sale', 'Sale')
)

# status = (
#     ('pending', 'pending'),
#     ('resolved', 'resolved')
# )


class PropertyRequest(models.Model):
    category = models.CharField(max_length=20, choices=Categories)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bedroom = models.PositiveIntegerField(default=0)
    more_info = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    # status = models.CharField(
    #     choices=status, max_length=10, default='published')
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Property Request"
        get_latest_by = ['created_at']

    def __str__(self):
        return str(self.id)
