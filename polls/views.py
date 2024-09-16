import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question, Vote
from django.contrib.auth import user_logged_in, \
                                user_login_failed, \
                                user_logged_out
from django.dispatch import receiver

logger = logging.getLogger("polls")


class IndexView(generic.ListView):
    """
    Display the latest five questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    Display a question and its choices.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Get the question object and render the template.

        Args:
            request: The HTTP request object.
            self.object (int): The ID of the question being voted on.

        Returns:
            HttpResponseRedirect: Redirects to the index page with an error
                                  message if the question is not published.
            HttpResponse: Renders the results page.
        """
        # Get the question object
        self.object = self.get_object()

        # Check if voting is allowed
        if not self.object.can_vote():
            messages.error(request, "This poll is closed.")
            return redirect('polls:index')

        return self.render_to_response(self.get_context_data(
                                        object=self.object))


class ResultsView(generic.DetailView):
    """
    Display the results of a question.
    """
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        Handel the Get request for the results view.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exists.")
            return redirect("polls:index")
        if not question.is_published():
            messages.error(request,
                           f"Poll number {question.id} Already closed.")
            return redirect("polls:index")
        return render(request, self.template_name, {"question": question})


@login_required
def vote(request, question_id):
    """
    Handles the user's vote for a poll question.
    """
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Http404 as ex:
        logger.exception(f"Non-existent question {question_id}: ", ex)
        raise

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        this_user = request.user
        logger.error(
            f"{this_user} submits vote without selecting a choice"
            f"on question {question}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    this_user = request.user
    logger.info(f"{this_user} submits vote on choice id:"
                f" {selected_choice.id} "
                f"on question id: {question.id}")
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update the vote after a user has changed their vote
        vote.choice = selected_choice
        vote.save()
    except Vote.DoesNotExist:
        # no matching vote - create a new vote object
        vote = Vote.objects.create(user=this_user, choice=selected_choice)
    messages.success(
            request, f"Your vote for '{selected_choice}' has been recorded.")
    return HttpResponseRedirect(
        reverse('polls:results', args=(question.id,)))


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    if request:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    return None


@receiver(user_logged_in)
def login_success(sender, request, user, **kwargs):
    """Log when user successfully login."""
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged in from {ip_addr}")


@receiver(user_logged_out)
def logout_success(sender, request, user, **kwargs):
    """Log when user successfully log out."""
    ip_addr = get_client_ip(request)
    logger.info(f"{user.username} logged out from {ip_addr}")


@receiver(user_login_failed)
def login_fail(sender, credentials, request, **kwargs):
    """Log when user failed to login."""
    ip_addr = get_client_ip(request)
    logger.warning(f"Failed login for {credentials['username']} \
from {ip_addr}")
