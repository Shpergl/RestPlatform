from __future__ import unicode_literals
from extuser.models import MyUser as User
from django.db import models

class Post(models.Model):

    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User)
    authorName = models.CharField(max_length=200)

    def create(self, user, title, text):
        if not user:
            raise ValueError('Users must be included')

        post = self.model(
            title=title,
            text=text,
            author=user,
            authorName=str(user.last_name + " " + user.first_name),
        )

        post.save(using=self._db)
        return post

    def __str__(self):
        return self.title
