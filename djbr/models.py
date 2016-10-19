from django.db import models

import datetime
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    pub_year = models.IntegerField('year published', default=2000)


    def was_published_recently(self):
        return self.pub_year >= timezone.now().year - 1
    
    def __str__(self):
        return "%s %s" % (self.title, self.pub_year)
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(default="")
    review_date = models.DateTimeField('review date')

    def __str__(self):
        return "%s %s" % (self.title, self.review_date)

class Author(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name
    
