from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ParticipantForm

# Teaching-only state: shared across browsers and lost when the server restarts.
participants = []


def is_christmas(request):
    today = timezone.localdate()
    context = {
        "today": today,
        "is_christmas": today.month == 12 and today.day == 25,
    }
    return render(request, "holiday/christmas.html", context)


def santa(request):
    form = ParticipantForm()
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if any(name.casefold() == person.casefold() for person in participants):
                form.add_error("name", "That name is already listed. Add a surname.")
            else:
                participants.append(name)
                return redirect("holiday:santa")

    context = {"form": form, "participants": participants}
    return render(request, "holiday/santa.html", context)
