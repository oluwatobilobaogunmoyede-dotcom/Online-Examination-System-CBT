from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from teachers.models import Teacher
from .models import Examination
from .forms import ExaminationForm


def can_manage_exams(user):
    return user.is_superuser or getattr(user, 'role', '') in ['admin', 'teacher']


def get_teacher_profile(user):
    try:
        return user.teacher
    except Teacher.DoesNotExist:
        return None


@login_required
@user_passes_test(can_manage_exams)
def examination_list(request):
    examinations = Examination.objects.select_related(
        'school_class', 'subject', 'teacher__user'
    ).order_by('-created_at')

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None:
            examinations = examinations.none()
        else:
            examinations = examinations.filter(teacher=teacher)

    return render(request, 'examinations/examination_list.html', {
        'examinations': examinations
    })


@login_required
@user_passes_test(can_manage_exams)
def examination_create(request):
    teacher = None

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None:
            return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = ExaminationForm(request.POST)

        if teacher:
            form.fields.pop('teacher', None)

        if form.is_valid():
            examination = form.save(commit=False)

            if teacher:
                examination.teacher = teacher

            examination.save()
            return redirect('examination_list')
    else:
        form = ExaminationForm()

        if teacher:
            form.fields.pop('teacher', None)

    return render(request, 'examinations/examination_form.html', {
        'form': form,
        'title': 'Create Examination'
    })


@login_required
@user_passes_test(can_manage_exams)
def examination_edit(request, pk):
    teacher = None

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None:
            return redirect('teacher_dashboard')

    if teacher:
        examination = get_object_or_404(
            Examination, pk=pk, teacher=teacher
        )
    else:
        examination = get_object_or_404(Examination, pk=pk)

    if request.method == 'POST':
        form = ExaminationForm(request.POST, instance=examination)

        if teacher:
            form.fields.pop('teacher', None)

        if form.is_valid():
            updated_exam = form.save(commit=False)

            if teacher:
                updated_exam.teacher = teacher

            updated_exam.save()
            return redirect('examination_list')
    else:
        form = ExaminationForm(instance=examination)

        if teacher:
            form.fields.pop('teacher', None)

    return render(request, 'examinations/examination_form.html', {
        'form': form,
        'title': 'Edit Examination'
    })


@login_required
@user_passes_test(can_manage_exams)
def examination_delete(request, pk):
    teacher = None

    if request.user.role == 'teacher' and not request.user.is_superuser:
        teacher = get_teacher_profile(request.user)

        if teacher is None:
            return redirect('teacher_dashboard')

    if teacher:
        examination = get_object_or_404(
            Examination, pk=pk, teacher=teacher
        )
    else:
        examination = get_object_or_404(Examination, pk=pk)

    if request.method == 'POST':
        examination.delete()
        return redirect('examination_list')

    return render(request, 'examinations/examination_confirm_delete.html', {
        'examination': examination
    })