from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import State, School, Subject


@staff_member_required
def admin_dashboard (request):
    return render(request, "admin/dashboard.html")


@staff_member_required
def addState (request):
    if request.method == "POST":
        name = request.POST.get("name")
        State.objects.create(
            name = name
        )
        return redirect(viewState)
    return render(request, "admin/addState.html")


@staff_member_required
def viewState(request):
    states = State.objects.all()
    return render(request, "admin/viewState.html", {"states":states})


@staff_member_required
def viewInstitute(request):
    state = State.objects.all()
    schools = School.objects.all()
    return render(request, "admin/viewInstitute.html", {
        "states":state,
        "schools":schools
    })


@staff_member_required
def viewSubject(request):
    subject = Subject.objects.all()
    return render(request, "admin/viewSubject.html", {"subjects":subject})


@staff_member_required
def addSubject(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Subject.objects.create(
            name = name
        )
        return redirect(viewSubject)
    return render(request, "admin/addSubject.html")


@staff_member_required
def approve_school(request, school_id):
    registration = School.objects.filter(id=school_id)
    if registration.exists():
        school = registration.first()
        school.is_verified = 'True'
        school.save()
    return redirect('viewInstitute')


@staff_member_required
def remove_school(request, school_id):
    registration = School.objects.filter(id=school_id)
    if registration.exists():
        school = registration.first()
        school.is_verified = 'False'
        school.save()
    return redirect('viewInstitute')


@staff_member_required
def delete_school(request, school_id):
    registration = School.objects.filter(id=school_id)
    if registration.exists():
        school = registration.first()
        if school.is_verified != "True":
            school.delete()
    return redirect('viewInstitute')

