from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.0


class QuestionManager(models.Manager):

    @staticmethod
    def update():
        questions = Question.manager.all()
        for q in questions:
            q.answers = Answer.manager.answer_count(q.id)
            q.likes = Like.manager.likes_of(q.id)
            q.save()

    def hot(self, num):
        Question.manager.update()
        return self.order_by('-likes')[:num].all()

    def new(self):
        Question.manager.update()
        return self.order_by('-id').all()

    def question_of_tag(self, tag_name):
        Question.manager.update()
        questions = self.filter(tags__title=tag_name).all()
        return questions

    def tags_of_question(self, q_id):
        Question.manager.update()
        return self.get(pk=q_id).tags.all()


class AnswerManager(models.Manager):

    @staticmethod
    def update(q_id):
        answers = Answer.manager.filter(question__id=q_id).all()
        for a in answers:
            a.likes = AnswerLike.manager.likes_of(a.id)
            a.save()

    def answers_of_question(self, q_id):
        Answer.manager.update(q_id)
        answers = self.filter(question__id=q_id).all()
        return answers

    def answer_count(self, q_id):
        return self.select_related('question').filter(question__id=q_id).count()


class AnswerLikeManager(models.Manager):
    def likes_of(self, item_id):
        likes = self.filter(answer__id=item_id).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0


class QuestionLikeManager(models.Manager):
    def likes_of(self, item_id):
        likes = self.filter(question__id=item_id).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0


class Question(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    likes = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)

    manager = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey('Question', models.PROTECT)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_correct = models.BooleanField()
    likes = models.IntegerField(default=0)

    manager = AnswerManager()

    def __str__(self):
        return f'Question {self.id}'


class Tag(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.title}'


class Profile(models.Model):
    avatar = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    val = models.SmallIntegerField(default=0)

    manager = QuestionLikeManager()


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey('Answer', on_delete=models.PROTECT)
    val = models.SmallIntegerField(default=0)

    manager = AnswerLikeManager()
