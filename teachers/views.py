
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import Q

from .models import Teacher
from .forms import TeacherForm

User = get_user_model()


def is_admin(user):
    return user.is_superuser or user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    search = request.GET.get('search', '')

    teachers = Teacher.objects.select_related('user').all()

    if search:
        teachers = teachers.filter(
            Q(employee_number__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )

    return render(request, 'teachers/teacher_list.html', {
        'teachers': teachers,
        'search': search,
    })


@login_required
@user_passes_test(is_admin)
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='teacher',
                )

                teacher = form.save(commit=False)
                teacher.user = user
                teacher.save()

            return redirect('teacher_list')
    else:
        form = TeacherForm()

    return render(request, 'teachers/teacher_form.html', {
        'form': form,
        'title': 'Register Teacher',
    })


@login_required
@user_passes_test(is_admin)
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)

        if form.is_valid():
            with transaction.atomic():
                user = teacher.user
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']

                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])

                user.save()
                form.save()

            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher, initial={
            'username': teacher.user.username,
            'first_name': teacher.user.first_name,
            'last_name': teacher.user.last_name,
            'email': teacher.user.email,
        })

    return render(request, 'teachers/teacher_form.html', {
        'form': form,
        'title': 'Edit Teacher',
    })


@login_required
@user_passes_test(is_admin)
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        teacher.user.delete()
        return redirect('teacher_list')

    return render(request, 'teachers/teacher_confirm_delete.html', {
        'teacher': teacher,
    })
