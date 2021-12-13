from team.models import Member
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.contrib.gis.geos import Point
from users.models import User
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from users.utils import random_uniquekey_generator, upload_property_document_path, upload_property_path, validate_document
# Create your models here.


Append = (
    ('daily', 'daily'),
    ('monthly', 'monthly'),
    ('yearly', 'yearly'),
    ('sqm',  'sqm'),
    ('instalment', 'Instalment'), 
    ('at once', 'At once'), 
    ("outright(one-off)", "outright(one-off)")
)

Purposes = (
    ('rent', 'Rent'),
    ('sale', 'sale'),     
)
status = (
    ('pending', 'pending'),
    ('published', 'published'),
    ('sold', 'sold'),
    ('flagged', 'flagged')
)


class PropertyType(models.Model):
    title = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(editable=False, null=True)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Property types"


class Feature(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(editable=False, null=True)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PropertyManager(models.Manager):
    def get_active_objects(self, user):
        if user.is_superuser:
            return super().get_queryset().order_by('-premium')
        return super().get_queryset().filter(active=True, status="published").order_by('-premium')
    # def get_queryset(self):
    #     return super(PropertyManager, self).get_queryset().filter(active=True, status="published").order_by('-premium')


class Property(models.Model):
    title = models.CharField(max_length=300)
    purpose = models.CharField(max_length=20, choices=Purposes)
    description = models.CharField(max_length=150, blank=True, null=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    bedroom = models.PositiveIntegerField(default=0)
    bathroom = models.PositiveIntegerField(default=0)
    parlour = models.PositiveIntegerField(default=0)
    kitchen = models.PositiveIntegerField(default=0)
    toilet = models.PositiveIntegerField(default=0)
    draft = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    append_to = models.CharField(max_length=30, choices=Append)
    premium = models.BooleanField(default=False)
    virtual_reality = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=10)
    document = ArrayField(models.CharField(max_length=20),
                          blank=True, null=True, size=10)
    video_link = models.URLField(blank=True, null=True)
    keyword = ArrayField(models.CharField(max_length=20),
                         blank=True, null=True, size=10)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    country = models.CharField(max_length=150)
    state = models.CharField(max_length=100, blank=True, null=True)
    lGA = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=150)
    # features = models.ManyToManyField(Feature, blank=True)
    features_fix = ArrayField(models.CharField(max_length=50, blank=True),
            size=50,blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False, null=True,
                            max_length=300, db_index=True)
    active = models.BooleanField(default=True)
    status = models.CharField(
        choices=status, max_length=10, default='published')
    views = models.PositiveIntegerField(default=0)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, blank=True)
    image_preview = models.CharField(max_length=500, blank=True, null=True)
    location = gis_models.PointField(default=Point(0, 0), blank=True)
    # draft_box = models.JSONField(default = dict)
    objects = models.Manager()
    active_objects = PropertyManager()

    def save(self, *args, **kwargs):
        value = self.title
        inputed_location = Point(
            float(self.longitude), float(self.latitude))
        slugified_value = slugify(value, allow_unicode=True)
        unique_key = random_uniquekey_generator()
        self.slug = f'{slugified_value}{unique_key}'
        self.location = inputed_location
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Agents' Properties"
        get_latest_by = ['created_at']

    def __str__(self):
        return str(self.id)

class Draft(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    draft_box = models.JSONField(default = dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    

    def __str__(self):
        return str(self.user)


class PropertyImage(models.Model):
    image = models.ImageField(upload_to=upload_property_path, validators=[
        validate_document])
    caption = models.CharField(max_length=50, blank=True, null=True)

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='property_image')


class Report(models.Model):
    user = models. ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class AssignPropertyToDeveloper(models.Model):
    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', related_name='developer_property', on_delete=models.CASCADE)
    assigned_team_member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.developer.email
class DetailPropertyAddress(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=500, blank=True, null=True)
    address = models.JSONField(default = dict)
    
    def __str__(self):
        return property.title

    
