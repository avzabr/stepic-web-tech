from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator, EmptyPage

from qa.forms import AskForm, AnswerForm
from qa.models import Question
from django.http import Http404

TYPE_NEW = 'new'
TYPE_POPULAR = 'popular'


@require_GET
def new(request):
    return main(request, type=TYPE_NEW)


@require_GET
def popular(request):
    return main(request, type=TYPE_POPULAR)


def main(request, type=TYPE_NEW):
    try:
        limit = int(request.GET.get('limit', 10))
        if limit > 1000:
            limit = 1000
    except ValueError:
        limit = 10
    try:
        p_n = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    questions = Question.objects.by_id().all() if type == TYPE_NEW else Question.objects.by_rating().all()

    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page='
    try:
        page = paginator.page(p_n)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render_to_response('main.html', {
        'q_list': page.object_list,
        'paginator': paginator,
        'page': page
    })


@require_GET
def question(request, id):
    q = get_object_or_404(Question, id=id)
    form = AnswerForm(initial={'question': q.id})

    return render(request, 'question.html', {
        'q': q,
        'answers': q.answer_set.all()[:],
        'form': form
    })


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            q = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'question_add.html', {
        'form': form
    })


@require_POST
def answer(request):
    form = AnswerForm(request.POST)
    if form.is_valid():
        a = form.save()
        url = a.question.get_url() + "?answer_added=True"
    else:
        url = '/question/' + form.data.get('question') + "?answer_added=False"
    return HttpResponseRedirect(url)
