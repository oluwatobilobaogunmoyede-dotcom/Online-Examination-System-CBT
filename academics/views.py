
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import SchoolClass, Subject
from .forms import SchoolClassForm, SubjectForm


def is_admin(user):
    return user.is_superuser or user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def class_list(request):
    classes = SchoolClass.objects.all().order_by('name')
    return render(request, 'academics/class_list.html', {
        'classes': classes
    })


@login_required
@user_passes_test(is_admin)
def class_create(request):
    if request.method == 'POST':
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = SchoolClassForm()

    return render(request, 'academics/class_form.html', {
        'form': form,
        'title': 'Add School Class'
    })


@login_required
@user_passes_test(is_admin)
def class_edit(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)

    if request.method == 'POST':
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = SchoolClassForm(instance=school_class)

    return render(request, 'academics/class_form.html', {
        'form': form,
        'title': 'Edit School Class'
    })


@login_required
@user_passes_test(is_admin)
def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)

    if request.method == 'POST':
        school_class.delete()
        return redirect('class_list')

    return render(request, 'academics/class_confirm_delete.html', {
        'school_class': school_class
    })


@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.select_related(
        'school_class', 'teacher__user'
    ).all().order_by('school_class__name', 'name')

    return render(request, 'academics/subject_list.html', {
        'subjects': subjects
    })


@login_required
@user_passes_test(is_admin)
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()

    return render(request, 'academics/subject_form.html', {
        'form': form,
        'title': 'Add Subject'
    })


@login_required
@user_passes_test(is_admin)
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)

    return render(request, 'academics/subject_form.html', {
        'form': form,
        'title': 'Edit Subject'
    })


@login_required
@user_passes_test(is_admin)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject.delete()
        return redirect('subject_list')

    return render(request, 'academics/subject_confirm_delete.html', {
        'subject': subject
    })
