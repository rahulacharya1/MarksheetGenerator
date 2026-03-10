from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import State, School


# ---------------- ADMIN DASHBOARD ----------------
@staff_member_required
def adminDashboard(request):
    return render(request, "admin/dashboard.html")


# ---------------- ADD STATE ----------------
@staff_member_required
def addState(request):

    if request.method == "POST":

        name = request.POST.get("name")

        if name:
            State.objects.create(name=name)

        return redirect("viewstate")

    return render(request, "admin/addState.html")


# ---------------- VIEW STATE ----------------
@staff_member_required
def viewState(request):

    states = State.objects.all()

    return render(request, "admin/viewState.html", {
        "states": states
    })


# ---------------- VIEW INSTITUTE ----------------
@staff_member_required
def viewInstitute(request):

    states = State.objects.all()

    schools = School.objects.all()

    return render(request, "admin/viewInstitute.html", {
        "states": states,
        "schools": schools
    })


# ---------------- APPROVE SCHOOL ----------------
@staff_member_required
def approveSchool(request, school_id):

    school = get_object_or_404(School, id=school_id)

    school.is_verified = True
    school.save()

    return redirect("viewinstitute")


# ---------------- REMOVE SCHOOL APPROVAL ----------------
@staff_member_required
def removeSchool(request, school_id):

    school = get_object_or_404(School, id=school_id)

    school.is_verified = False
    school.save()

    return redirect("viewinstitute")


# ---------------- DELETE SCHOOL ----------------
@staff_member_required
def deleteSchool(request, school_id):

    school = get_object_or_404(School, id=school_id)

    if not school.is_verified:
        school.delete()

    return redirect("viewinstitute")

