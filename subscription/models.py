from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from users.utils import random_uniquekey_generator
from users.models import Agent, User
# Create your models here.

# from users.models import Agent


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer')
    customer_code = models.CharField(
        max_length=50, db_index=True)
    def __str__(self):
        return self.user


class MembershipPlanFeatures(models.Model):
    listing = models.PositiveIntegerField(
        default=1, help_text="Maximum Number of listing a user have")
    premium_listing = models.PositiveIntegerField(
        default=0, help_text="Maximum Number of Premium listing a user have")


class MembershipPlan(models.Model):
    INTERVALS_CHOICES = (
        ('daily', 'daily'),
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('quarterly', 'quarterly'),
        ('annually', 'annually'),
    )
    interval = models.CharField(choices=INTERVALS_CHOICES,
                                max_length=10,
                                blank=True,
                                null=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100, decimal_places=4, default=0.0)
    membership_features = models.OneToOneField(MembershipPlanFeatures, on_delete=models.CASCADE,
                                               primary_key=True)
    plan_code = models.CharField(db_index=True, max_length=100, validators=[
                                 MinValueValidator(1000)])
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_final_cost(self):
    #     return self.discount * (self.price / Decimal(100))
    class Meta:
        verbose_name_plural = "Membership Plan"
        get_latest_by = ['created_at']

    def save(self, *args, **kwargs):
        sluuged_name = slugify(self.name)
        self.slug = f'{self.plan_code}'
        super(MembershipPlan, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class userMembershipFeatures(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_features')
    listing = models.PositiveIntegerField(
        default=1, help_text="Maximum Number of listing a user have")
    premium_listing = models.PositiveIntegerField(
        default=0, help_text="Maximum Number of Premium listing a user have")

    def __str__(self):
        return self.user


class Subscription(models.Model):
    agent = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    subscription_plan = models.ForeignKey(
        MembershipPlan, on_delete=models.CASCADE, null=True)
    subscription_code = models.CharField(max_length=40)
    email_token = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    # @property
    # def get_created_date(self):
    #     subscription = stripe.Subscription.retrieve(
    #         self.stripe_subscription_id)
    #     return datetime.fromtimestamp(subscription.created)

    # @property
    # def get_next_billing_date(self):
    #     subscription = stripe.Subscription.retrieve(
    #         self.stripe_subscription_id)
    #     return datetime.fromtimestamp(subscription.current_period_end)
