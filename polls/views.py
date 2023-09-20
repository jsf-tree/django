from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

# For 404 errors
from django.http import Http404

# To avoid racing conditions
from django.db.models import F

# Django provides shortcuts for very common idiom like:
#  render - load a template, fill a context and return an HttpResponse object with the result of the rendered template
#  get_object_or_404 - use get() and raise Http404 if the object doesnt exist
#  get_list_or_404 - use filter() and raise Http404 if the list is empty
from django.shortcuts import get_object_or_404, render     



from .models import Question, Choice


def index(request):
    # --- More verbose way --- #
    #latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #template = loader.get_template('polls/index.html')
    ## Context is a dictionary mapping template variable names to Python objects
    #context = {"latest_question_list": latest_question_list}
    #return HttpResponse(template.render(context, request))

    # --- Shortcut way --- #
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)   # polls/index.html is namespaces (inside templates, there is a folder with the app_name)


def detail(request, question_id):
    # --- More verbose way --- #
    #  This introduces tight coupling between Views and Models.
    #  In Django loose coupling philosophy, views should not directly
    #  operate data (models). The method "get_object_or_404" is thus
    #  preferred.
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    #return render(request, "polls/detail.html", {"question": question})

    # --- Shortcut way --- #
    #  More than a shortcut, aligned with Django's loose coupling philosophy
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # F() runs a SQL to avoid racing conditions between simultanesouly user requests
        selected_choice.votes = F('votes') + 1  
        selected_choice.save()
        selected_choice.refresh_from_db()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))