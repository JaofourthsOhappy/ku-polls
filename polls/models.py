"""Module for using in models."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Class of question.

    ...

    Attributes
    ----------
    question_text : CharField
        text of the question.
    pub_date : DateTimeField
        published date of question
    end_date : DateTimeField
        end date of the question

    Methods
    -------
    was_published_recently()
        check if question now published or not.

    is_published()
        check if the question is published yet.

    can_vote()
        check if the question can vote or not.

    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(
        'date end', default=timezone.now() + datetime.timedelta(days=1))
    previous_vote = models.CharField(max_length=200, default="")

    def __str__(self):
        """
        Sting method.

        Return:
        question text
        """
        return self.question_text

    def was_published_recently(self):
        """
        Check whether it recently published or not.

        Return:
        True if the question is recently published, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """
        Check whether it published or not.

        Return:
        True if the question is published, False otherwise.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        Check whether it can vote or not.

        Return:
        True if the question can vote, False otherwise.
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Class of choice."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Sting method.

        Return:
        choice text
        """
        return self.choice_text


class Vote(models.Model):
    """Class of the user vote."""

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)