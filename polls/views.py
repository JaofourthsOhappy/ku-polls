from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
# from django.http import Http404
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get(self, request, **kwargs):
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.can_vote() :
                return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "This poll is already closed. Can't vote!!!"))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('polls:index'), messages.error(request, "This poll is not exist."))
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(object=self.get_object()))

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return HttpResponseRedirect(reverse('polls:index'), messages.error("Can't vote after poll closed."))
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice.", })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))