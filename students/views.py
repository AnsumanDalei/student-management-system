from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def superuser_required(view_func):
    return user_passes_test(lambda user: user.is_authenticated and user.is_superuser)(view_func)


@login_required
def home(request):
    search = request.GET.get('search', '').strip()
    course = request.GET.get('course', '').strip()

    students = Student.objects.all()
    if search:
        students = students.filter(
            Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(course__icontains=search)
        )
    if course:
        students = students.filter(course=course)

    paginator = Paginator(students, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'students/home.html', {
        'students': page_obj,
        'page_obj': page_obj,
        'search': search,
        'course': course,
        'total_students': Student.objects.count(),
        'course_choices': Student.COURSE_CHOICES,
    })


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'students/add_student.html', {'form': form})


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {
        'form': form,
        'student': student,
    })


@login_required
def view_student(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, 'students/view_student.html', {'student': student})


@superuser_required
def delete_student_page(request):
    students = Student.objects.all()
    return render(request, 'students/delete_student.html', {'students': students})


@superuser_required
def delete_student(request, id):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=id)
        student.delete()
    return redirect('delete_student_page')
