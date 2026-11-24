
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Question
from .forms import QuestionForm
from teachers.models import Teacher


def can_manage_questions(user):
    return user.is_superuser or user.role in ['admin', 'teacher']


def get_teacher_profile(user):
    try:
        return user.teacher
    except Teacher.DoesNotExist:
        return None


@login_required
@user_passes_test(can_manage_questions)
def question_list(request):
    questions = Question.objects.select_related(
        'examination'
    ).all().order_by('-created_at')

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)
        if teacher is None:
            return redirect('dashboard')
        questions = questions.filter(examination__teacher=teacher)

    return render(
        request,
        'questions/question_list.html',
        {'questions': questions}
    )


@login_required
@user_passes_test(can_manage_questions)
def question_create(request):
    teacher = None

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)
        if teacher is None:
            return redirect('dashboard')

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)

            if teacher and question.examination.teacher_id != teacher.id:
                form.add_error(
                    'examination',
                    'You can only add questions to your own examinations.'
                )
            else:
                question.save()
                return redirect('question_list')
    else:
        form = QuestionForm()

        if teacher:
            form.fields['examination'].queryset = (
                form.fields['examination'].queryset.filter(teacher=teacher)
            )

    return render(
        request,
        'questions/question_form.html',
        {'form': form, 'title': 'Add Question'}
    )


@login_required
@user_passes_test(can_manage_questions)
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    teacher = None

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None or question.examination.teacher_id != teacher.id:
            return redirect('question_list')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            updated_question = form.save(commit=False)

            if teacher and updated_question.examination.teacher_id != teacher.id:
                form.add_error(
                    'examination',
                    'You can only use your own examinations.'
                )
            else:
                updated_question.save()
                return redirect('question_list')
    else:
        form = QuestionForm(instance=question)

        if teacher:
            form.fields['examination'].queryset = (
                form.fields['examination'].queryset.filter(teacher=teacher)
            )

    return render(
        request,
        'questions/question_form.html',
        {'form': form, 'title': 'Edit Question'}
    )


@login_required
@user_passes_test(can_manage_questions)
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None or question.examination.teacher_id != teacher.id:
            return redirect('question_list')

    if request.method == 'POST':
        question.delete()
        return redirect('question_list')

    return render(
        request,
        'questions/question_confirm_delete.html',
        {'question': question}
    )
