from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q

from .models import Student
from .forms import StudentForm

User = get_user_model()


def is_admin(user):
    return user.is_superuser or user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def student_list(request):
    search = request.GET.get('search', '')

    students = Student.objects.select_related('user').all()

    if search:
        students = students.filter(
            Q(admission_number__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )

    return render(request, 'students/student_list.html', {
        'students': students,
        'search': search,
    })


@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='student',
                )

                student = form.save(commit=False)
                student.user = user
                student.save()

            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Register Student',
    })


@login_required
@user_passes_test(is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            with transaction.atomic():
                user = student.user
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])

                user.save()
                form.save()

            return redirect('student_list')
    else:
        form = StudentForm(instance=student, initial={
            'username': student.user.username,
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'email': student.user.email,
        })

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Edit Student',
    })


@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.user.delete()
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {
        'student': student,
    })
