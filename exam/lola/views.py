from django.shortcuts import render_to_response
import random
import difflib
from django.template import RequestContext
from django import forms
from .models import Participant, Question, Answer


class AnswerForm(forms.Form):
    answer = forms.CharField(max_length=256)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def learning(request):
    context_vars = {}

    participant_id = request.session.get('participant_id', False)
    if participant_id:
        participant = Participant.objects.get(id=participant_id)
        queue = map(int, participant.queue.split(','))
    else:
        participant = Participant.objects.create(ip=get_client_ip(request))
        queue = list(Question.objects.all().values_list('id', flat=True)) * 3
        random.shuffle(queue)
        participant.queue = ','.join(map(str, queue))
        participant.save()
        request.session['participant_id'] = participant.id

    prev_question = None
    answer = None
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            prev_question = Question.objects.get(id=queue.pop(0))
            form_answer = form.cleaned_data.get('answer')
            ratio = difflib.SequenceMatcher(None, form_answer.lower(), prev_question.answer.lower()).ratio()
            answer = Answer()
            answer.participant = participant
            answer.question = prev_question
            answer.answer = form_answer
            answer.ratio = ratio
            if ratio > .8:
                answer.valid = True
            else:
                answer.valid = False
                queue.insert(2, prev_question.id)

            participant.queue = ','.join(map(str, queue))
            answer.save()
            form = AnswerForm()

    else:
        form = AnswerForm()

    participant.save()
    try:
        question = Question.objects.get(id=queue[0])
    except IndexError:
        question = None
        del request.session['participant_id']

    context_vars.update({
        'form': form,
        'question': question,
        'prev_question': prev_question,
        'answer': answer,
        'participant': participant,
        'queue': queue,
    })

    return render_to_response('lola/learning.html', context_vars, context_instance=RequestContext(request))
