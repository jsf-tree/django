from django.http import HttpResponse
from django.template import loader

# For 404 errors
from django.http import Http404

# Django provides shortcuts for very common idiom like:
#  render - load a template, fill a context and return an HttpResponse object with the result of the rendered template
#  get_object_or_404 - use get() and raise Http404 if the object doesnt exist
#  get_list_or_404 - use filter() and raise Http404 if the list is empty
from django.shortcuts import get_object_or_404, render     



from .models import Question


def index(request):
    # --- More verbose way --- #
    #latest_question_list = Question.objects.order_by("-pub_date")[:5]
    #template = loader.get_template('polls/index.html')
    ## Context is a dictionary mapping template variable names to Python objects
    #context = {"latest_question_list": latest_question_list}
    #return HttpResponse(template.render(context, request))

    # --- Shortcut way --- #
    return render(request, "polls/index.html", context)


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
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)