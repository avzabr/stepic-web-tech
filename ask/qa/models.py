import string
from datetime import datetime, timedelta
import random

from django.db import models
from django.core.urlresolvers import reverse


class User(models.Model):
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField()


class Session(models.Model):
    key = models.CharField(unique=True, max_length=100)
    user = models.ForeignKey(User)
    expires = models.DateTimeField()


class QuestionManager(models.Manager):
    def by_id(self):
        return self.order_by('-id')

    def by_rating(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True)
    author = models.ForeignKey(User, related_name='question_author_set')
    likes = models.ManyToManyField(User, related_name='question_likes_set')
    objects = QuestionManager()

    def get_url(self):
        return reverse('question', kwargs={'id': str(self.id)})

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


def generate_long_random_key():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(40))


def salt_and_hash(password):
    import hashlib

    SALT = 'STEPIC'
    return hashlib.sha512(password + SALT).hexdigest()


def do_login(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    hashed_pass = salt_and_hash(password)
    if user.password != hashed_pass:
        return None
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key


def do_signup(username, password, email):
    user = User.objects.create(username=username, password=salt_and_hash(password), email=email)
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key
