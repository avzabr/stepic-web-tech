from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def by_id(self):
        return self.order_by('-id')

    def by_rating(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    author = models.ForeignKey(User, related_name='question_author_set')
    likes = models.ManyToManyField(User, related_name='question_likes_set')
    objects = QuestionManager()

    def get_url(self):
        return reverse('question', kwargs={id: self.id})

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'questions'
        ordering = ['-added_at']


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.text

    class Meta:
        db_table = 'answers'
