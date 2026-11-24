@login_required
def admin_dashboard(request):

    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')

    return render(request, 'admin/dashboard.html')


@login_required
def teacher_dashboard(request):

    if request.user.role != 'teacher':
        return redirect('dashboard')

    return render(request, 'teachers/dashboard.html')


@login_required
def student_dashboard(request):

    if request.user.role != 'student':
        return redirect('dashboard')

    return render(request, 'students/dashboard.html')