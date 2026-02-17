from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import States, Schools


@staff_member_required
def admin_dashboard (request):
    return render(request, "admin/dashboard.html")


@staff_member_required
def addState (request):
    if request.method == "POST":
        name = request.POST.get("name")
        States.objects.create(
            name = name
        )
        return redirect(viewState)
    return render(request, "admin/addState.html")


@staff_member_required
def viewState(request):
    states = States.objects.all()
    return render(request, "admin/viewState.html", {"states":states})


@staff_member_required
def viewInstitute(request):
    state = States.objects.all()
    schools = Schools.objects.all()
    return render(request, "admin/viewInstitute.html", {
        "states":state,
        "schools":schools
    })

