import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    A question that can be voted on.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('ending date', null=True, blank=True)

    def was_published_recently(self):
        """
        Checks if the question was published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def is_published(self):
        """
        Checks if the question is published.
        :return: True if the question is published, False otherwise.
        """
        return self.pub_date < timezone.now()

    def can_vote(self):
        """
        Checks if the question can be voted on.
        """
        if self.is_published():
            return self.end_date is None or self.end_date >= timezone.now()

    def __str__(self):
        """
        Returns a string representation of the question.
        """
        return self.question_text


class Choice(models.Model):
    """
    A choice for a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def votes(self):
        """
        Returns the number of votes for this choice.
        """
        return self.vote_set.count()

    def user_voted(self):
        """return all the users that have voted on this choice"""
        return (vote.user for vote in self.vote_set.all())

    def __str__(self):
        """
        Returns a string representation of the choice.
        """
        return self.choice_text


class Vote(models.Model):
    """Record a choice for a question made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.choice} by {self.user}"
