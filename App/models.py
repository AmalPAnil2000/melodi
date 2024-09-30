from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Lyrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    keyword = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    verse1 = models.TextField(blank=True)
    chorus = models.TextField(blank=True)
    verse2 = models.TextField(blank=True)
    bridge = models.TextField(blank=True)
    outro = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.genre} lyrics for '{self.keyword}'"
    

class LyricsGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    generation_count = models.PositiveIntegerField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.keyword} - {self.generation_count}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Music(models.Model):
    CATEGORY_CHOICES = [
        ('pop', 'Pop'),
        ('hip-hop', 'Hip-Hop'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
        # Add more categories as needed
    ]
    
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    music_file = models.FileField(upload_to='music/')
    cover_image = models.ImageField(upload_to='covers/',blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # Choices for the category field
    file = models.FileField(upload_to='music/', default='path/to/placeholder.mp3')
    date_added = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.title