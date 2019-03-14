from django.contrib.auth.models import User
from django.db import models

from configs import random_code, BID_STATUS, QUOTE_STATUS


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    lead = models.ForeignKey(User, on_delete=models.SET(1))
    description = models.TextField()
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField(max_length=55)
    bidding = models.BooleanField(default=False, blank=True)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    document = models.FileField(upload_to='documents')
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectEquipment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_cost = models.FloatField()
    unit_cost_in = models.CharField(max_length=55)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    measurement_in = models.CharField(max_length=55)
    weight = models.FloatField()
    weight_in = models.CharField(max_length=55)
    estimated_quantity = models.FloatField()
    description = models.TextField()
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectBudget(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    unit_cost = models.FloatField()
    unit_cost_in = models.CharField(max_length=55)
    description = models.TextField()
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectBid(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_status = models.CharField(max_length=68, choices=BID_STATUS, blank=False, default='Open')
    slug = models.SlugField(null=True, db_index=True, blank=True)
    rfq = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.vendor.first_name} {self.vendor.last_name}'


class ProjectQuote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.project.name}'


class ProjectQuoteItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quote = models.ForeignKey(ProjectQuote, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(ProjectEquipment, on_delete=models.CASCADE)
    quote_status = models.CharField(max_length=68, choices=QUOTE_STATUS, blank=False, default='Open')
    quote_price = models.FloatField(default=0)
    slug = models.SlugField(null=True, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['quote_price']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.equipment.name}'