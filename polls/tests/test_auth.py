import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
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


class AuthenticationTest(TestCase):
    """Class for testing the user authentication."""

    def setUp(self):
        """Method for setting up the user for testing the authentication."""
        User = get_user_model()
        user = User.objects.create_user("Pazcal", email="sahanon.p@ku.th", password="782543")
        user.first_name = "Sahanon"
        user.last_name = "Phisetpakasit"
        user.save()

    def test_login(self):
        """Test the user login."""
        self.client.login(username="Pazcal", password="782543")
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 200)
        self.assertContains(respone, "Sahanon")

    def test_logout(self):
        """Test the user logout."""
        self.client.login(username="Pazcal", password="782543")
        self.client.logout()
        url = reverse("polls:index")
        respone = self.client.get(url)
        self.assertNotContains(respone, "Sahanon")

    def test_authenticate_vote(self):
        """Test the user vote."""
        self.client.login(username="Pazcal", password="782543")
        question = create_question(question_text='This is a question', days=-5)
        response = self.client.get(reverse('polls:vote', args=(question.id,)))
        self.assertEqual(response.status_code, 200)
