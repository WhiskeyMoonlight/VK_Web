from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Question(models.Model):
    question_title = models.CharField(max_length=128)
    question_body = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions', null=True, blank=True)
    like = models.OneToOneField('Like', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Answer(models.Model):
    question = models.ForeignKey('Question', models.PROTECT)
    answer_body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_correct = models.BooleanField()


class Tag(models.Model):
    tag_title = models.CharField(max_length=32)


class Profile(models.Model):
    avatar = models.ImageField(upload_to='../static/img/')
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Like(models.Model):
    count = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)