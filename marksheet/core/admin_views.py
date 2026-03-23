from django.shortcuts import render, redirect
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
            if not State.objects.filter(name__iexact=name).exists():
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
    state_id = request.GET.get("state")
    if state_id:
        schools = School.objects.filter(state_id=state_id)
    else:
        schools = School.objects.all()
    return render(request, "admin/viewInstitute.html", {
        "states": state_id,
        "schools": schools
    })


# ---------------- APPROVE SCHOOL ----------------
@staff_member_required
def approveSchool(request, school_id):
    school = School.objects.filter(id=school_id).first()
    if not school:
        return redirect("viewinstitute")

    school.is_verified = True
    school.save()
    return redirect("viewinstitute")


# ---------------- REMOVE SCHOOL APPROVAL ----------------
@staff_member_required
def removeSchool(request, school_id):
    school = School.objects.filter(id=school_id).first()
    if not school:
        return redirect("viewinstitute")

    school.is_verified = False
    school.save()
    return redirect("viewinstitute")


# ---------------- DELETE SCHOOL ----------------
@staff_member_required
def deleteSchool(request, school_id):
    school = School.objects.filter(id=school_id).first()
    if not school:
        return redirect("viewinstitute")

    if not school.is_verified:
        school.delete()
    return redirect("viewinstitute")

