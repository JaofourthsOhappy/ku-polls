from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
# from django.http import Http404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Question, Choice, Vote

from datetime import datetime
from django.dispatch import receiver


class IndexView(generic.ListView):
    """Index View Class."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be published in the future).
        Returns: Last Five Questions
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail View."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Result View."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Vote Function If no vote return to page before and print the message."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=request.user).exists():
            vote = question.vote_set.get(user=request.user)
            vote.choice = selected_choice
            vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
