from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги'),
        ('other', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('used', 'Б/у')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    image_url = models.ImageField(upload_to='images/ads/%Y/%m/%d/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title