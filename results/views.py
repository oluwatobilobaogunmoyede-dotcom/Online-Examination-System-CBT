
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from examinations.models import Examination
from questions.models import Question
from .models import ExamAttempt, StudentAnswer


def is_student(user):
    return user.is_authenticated and user.role == 'student'


@login_required
def available_examinations(request):
    if not is_student(request.user):
        return redirect('dashboard')

    examinations = Examination.objects.filter(
        is_published=True
    ).order_by('start_time')

    return render(
        request,
        'results/available_examinations.html',
        {'examinations': examinations}
    )


@login_required
def start_examination(request, pk):
    if not is_student(request.user):
        return redirect('dashboard')

    if request.method != 'POST':
        return redirect('available_examinations')

    examination = get_object_or_404(
        Examination,
        pk=pk,
        is_published=True
    )

    now = timezone.now()

    if now < examination.start_time:
        return redirect('available_examinations')

    if now >= examination.end_time:
        return redirect('available_examinations')

    attempt, created = ExamAttempt.objects.get_or_create(
        student=request.user,
        examination=examination
    )

    if attempt.is_submitted:
        return redirect('available_examinations')

    return redirect('take_examination', pk=attempt.pk)


@login_required
def take_examination(request, pk):
    if not is_student(request.user):
        return redirect('dashboard')

    attempt = get_object_or_404(
        ExamAttempt.objects.select_related('examination'),
        pk=pk,
        student=request.user
    )

    if attempt.is_submitted:
        return redirect('available_examinations')

    examination = attempt.examination

    duration_deadline = (
        attempt.started_at +
        timedelta(minutes=examination.duration)
    )

    deadline = min(
        duration_deadline,
        examination.end_time
    )

    questions = Question.objects.filter(
        examination=examination
    ).order_by('id')

    if request.method == 'POST':
        total_score = 0

        for question in questions:
            selected = request.POST.get(
                f'question_{question.id}', ''
            )

            if selected not in ['A', 'B', 'C', 'D']:
                selected = ''

            is_correct = selected == question.correct_option

            marks = question.marks if is_correct else 0

            StudentAnswer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    'selected_option': selected,
                    'is_correct': is_correct,
                    'marks_awarded': marks,
                }
            )

            total_score += marks

        attempt.score = total_score
        attempt.is_submitted = True
        attempt.submitted_at = timezone.now()
        attempt.save()

        return redirect('result_detail', pk=attempt.pk)

    remaining_seconds = max(
        0,
        int((deadline - timezone.now()).total_seconds())
    )

    if remaining_seconds <= 0:
        return redirect('available_examinations')

    return render(
        request,
        'results/take_examination.html',
        {
            'attempt': attempt,
            'examination': examination,
            'questions': questions,
            'remaining_seconds': remaining_seconds,
        }
    )


@login_required
def result_detail(request, pk):
    if not is_student(request.user):
        return redirect('dashboard')

    attempt = get_object_or_404(
        ExamAttempt.objects.select_related('examination'),
        pk=pk,
        student=request.user,
        is_submitted=True
    )

    answers = StudentAnswer.objects.filter(
        attempt=attempt
    ).select_related('question')

    total_questions = attempt.examination.questions.count()

    return render(
        request,
        'results/result_detail.html',
        {
            'attempt': attempt,
            'answers': answers,
            'total_questions': total_questions,
        }
    )
