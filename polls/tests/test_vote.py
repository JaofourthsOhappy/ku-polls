from unittest import TestCase
from polls.models import Question
from django.utils import timezone
import datetime
class TestVoteAndPublished(TestCase):
    """Class for testing the is_published and can_vote."""

    def test_is_published(self):
        """Check for normal is_published."""
        time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=time)
        self.assertTrue(question.is_published())

    def test_is_published_with_not_published_question(self):
        """Check is_published with not published question."""
        end_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=end_time)
        self.assertFalse(question.is_published())

    def test_can_vote(self):
        """Check for normal can_vote."""
        pub_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertTrue(question.can_vote())

    def test_can_vote_after_question(self):
        """Check if the question can vote after the end date."""
        pub_time = timezone.now() - datetime.timedelta(days=2)
        end_time = timezone.now() - datetime.timedelta(days=1)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.can_vote())

    def test_can_vote_before_question(self):
        """Check if the question can vote before the published date."""
        pub_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=pub_time)
        self.assertFalse(question.can_vote())
