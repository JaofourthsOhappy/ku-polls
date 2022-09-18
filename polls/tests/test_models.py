import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question

def create_question(question_text, days):
    """Create the sample question.

    Parameters
    ----------
    question_text : str
        Text of the sample question
    days : datetime
        The published date
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTest(TestCase):
    """Class for testing the question model."""

    def test_was_published_recently_with_future_question(self):
        """Check if it's published recently with the future question."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Check if it's published recently with the old question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Check if it's published recently with the recent question."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
