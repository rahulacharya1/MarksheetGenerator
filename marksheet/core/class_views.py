from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import School, ClassRoom
from .decorators import school_required


# ---------------- MANAGE CLASS ----------------
@login_required
@school_required
def manageClass(request):
    return render(request, 'institute/class/manageclass.html')


# ---------------- ADD CLASS ----------------
@login_required
@school_required
def addclass(request):
    school = School.objects.get(user=request.user)

    if request.method == "POST":
        classname = request.POST.get("classname")
        section = request.POST.get("section")

        try:
            classname = int(classname)
        except (ValueError, TypeError):
            return render(request, "institute/class/addclass.html", {
                "school": school,
                "error": "Class must be a number between 1 and 10."
            })

        if classname < 1 or classname > 10:
            return render(request, "institute/class/addclass.html", {
                "school": school,
                "error": "Class must be between 1 and 10 only."
            })

        if section not in ["A", "B"]:
            return render(request, "institute/class/addclass.html", {
                "school": school,
                "error": "Section must be A or B only."
            })

        if ClassRoom.objects.filter(school=school, name=classname, section=section).exists():
            return render(request, "institute/class/addclass.html", {
                "school": school,
                "error": "This class already exists."
            })

        ClassRoom.objects.create(
            school=school,
            name=classname,
            section=section
        )
        return redirect('viewclass')

    return render(request, "institute/class/addclass.html", {
        "school": school
    })


# ---------------- VIEW CLASS ----------------
@login_required
@school_required
def viewclass(request):
    school = School.objects.get(user=request.user)
    classroom = ClassRoom.objects.filter(school=school)

    return render(request, "institute/class/viewclass.html", {
        "allclass": classroom,
        "school": school
    })

