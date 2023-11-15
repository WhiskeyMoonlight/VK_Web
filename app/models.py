from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count


# Create your models here.0

def best_users():
    users = User.objects.all()
    best_users_list = []
    for user in users:
        rating = (Question.manager.get_all_likes(user.id)
                  + Answer.manager.get_all_likes(user.id))
        user_struct = {
            'user': user.id,
            'username': user.username,
            'rating': rating
        }
        best_users_list.append(user_struct)
    best_users_list.sort(key=lambda _dict: _dict['rating'])
    return best_users_list[:5]


class QuestionManager(models.Manager):

    @staticmethod
    def update():
        questions = Question.manager.all()
        for q in questions:
            q.answers = Answer.manager.answer_count(q.id)
            q.likes = Like.manager.likes_of(q.id)
            q.save()

    @staticmethod
    def update_user_questions(u_id):
        questions = Question.manager.filter(user__id=u_id)
        for q in questions:
            q.answers = Answer.manager.answer_count(q.id)
            q.likes = Like.manager.likes_of(q.id)
            q.save()

    def hot(self):
        # Question.manager.update()
        return self.order_by('-likes').all()

    def new(self):
        # Question.manager.update()
        return self.order_by('-id').all()

    def question_of_tag(self, tag_name):
        Question.manager.update()
        questions = self.filter(tags__title=tag_name).all()
        return questions

    def tags_of_question(self, q_id):
        Question.manager.update()
        return self.get(pk=q_id).tags.all()

    def questions_of_user(self, u_id):
        Question.manager.update_user_questions(u_id)
        return self.filter(user__id=u_id).all()

    @staticmethod
    def get_all_likes(u_id):
        questions = Question.manager.questions_of_user(u_id)
        likes = questions.aggregate(Sum('likes')).get('likes__sum')
        if likes:
            return likes
        return 0


class AnswerManager(models.Manager):

    @staticmethod
    def update(q_id):
        answers = Answer.manager.filter(question__id=q_id).all()
        for a in answers:
            a.likes = AnswerLike.manager.likes_of(a.id)
            a.save()

    @staticmethod
    def update_user_answers(u_id):
        answers = Answer.manager.filter(user__id=u_id).all()
        for a in answers:
            a.likes = AnswerLike.manager.likes_of(a.id)
            a.save()

    def answers_of_question(self, q_id):
        Answer.manager.update(q_id)
        answers = self.filter(question__id=q_id).all()
        return answers

    def answer_count(self, q_id):
        return self.select_related('question').filter(question__id=q_id).count()

    def answers_of_user(self, u_id):
        Answer.manager.update_user_answers(u_id)
        return self.filter(user__id=u_id).all()

    @staticmethod
    def get_all_likes(u_id):
        answers = Answer.manager.answers_of_user(u_id)
        likes = answers.aggregate(Sum('likes')).get('likes__sum')
        if likes:
            return likes
        return 0


class QuestionLikeManager(models.Manager):
    def likes_of(self, item_id):
        likes = self.filter(question__id=item_id).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0


class AnswerLikeManager(models.Manager):
    def likes_of(self, item_id):
        likes = self.filter(answer__id=item_id).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0


class TagManager(models.Manager):

    def popular_tags(self):
        return self.annotate(num_questions=Count('questions')).order_by('-num_questions')[:5]


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

    class Meta:
        ordering = ['-id']

    manager = AnswerManager()

    def __str__(self):
        return f'Question {self.id}'


class Tag(models.Model):
    title = models.CharField(max_length=32)

    manager = TagManager()

    def __str__(self):
        return f'{self.title}'


class Profile(models.Model):
    avatar = models.CharField(max_length=128)
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    CHOICES = (
        ('l', 1),
        ('n', 0),
        ('d', -1)
    )
    val = models.SmallIntegerField(default=0, choices=CHOICES)

    class Meta:
        unique_together = [['user', 'question']]

    manager = QuestionLikeManager()


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey('Answer', on_delete=models.PROTECT)
    CHOICES = (
        ('l', 1),
        ('n', 0),
        ('d', -1)
    )
    val = models.SmallIntegerField(default=0, choices=CHOICES)

    class Meta:
        unique_together = [['user', 'answer']]

    manager = AnswerLikeManager()
