from django.contrib.auth.models import User
from django.db import models


# Create your models here.0


class QuestionManager(models.Manager):
    def hot_questions(self, num):
        return self.order_by('-likes')[:num].values()

    def new_questions(self, num):
        return self.order_by('-id')[:num].values()

    # def question_of_tag(self, tag_name):
    #     tagged = []
    #     for Q in QUESTIONS:
    #         if tag_name in Q['tags']:
    #             tag_questions.append(Q)
    #     for question in self.values():
    #         if tag_name in Tag.objects.all_tags():
    #             Tag.objects.tag_id(tag_name)
    #     return tagged


class TagManager(models.Manager):
    def all_tags(self):
        return self.values()

    def tag_id(self, tag_name):
        return self.filter(tag_title=tag_name)[0].id


class Question(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    likes = models.IntegerField(default=0)

    question_items = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey('Question', models.PROTECT)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_correct = models.BooleanField()

    def __str__(self):
        return f'Question {self.id}'


class Tag(models.Model):
    title = models.CharField(max_length=32)

    objects = TagManager()

    def __str__(self):
        return f'{self.title}'


class Profile(models.Model):
    avatar = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    val = models.SmallIntegerField(default=0)
