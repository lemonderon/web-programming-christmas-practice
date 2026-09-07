import random

from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ParticipantForm

# Teaching-only state: shared across browsers and lost when the server restarts.
participants = []
pairs = []


def is_christmas(request):
    today = timezone.localdate()
    context = {
        "today": today,
        "is_christmas": today.month == 12 and today.day == 25,
    }
    return render(request, "holiday/christmas.html", context)


def make_pairs(participants):
    """Make a gift circle from at least two distinct names."""
    shuffled = participants.copy()
    random.shuffle(shuffled)
    return [
        [giver, shuffled[(index + 1) % len(shuffled)]]
        for index, giver in enumerate(shuffled)
    ]


def santa(request):
    action = request.POST.get("action")
    form = ParticipantForm(request.POST if action == "add" else None)
    error = ""

    if request.method == "POST":
        if action == "add":
            if form.is_valid():
                name = form.cleaned_data["name"]
                if any(name.casefold() == person.casefold() for person in participants):
                    form.add_error("name", "That name is already listed. Add a surname.")
                else:
                    participants.append(name)
                    pairs.clear()
                    return redirect("holiday:santa")
        elif action == "draw":
            if len(participants) < 2:
                error = "Add at least two participants before drawing."
            else:
                pairs[:] = make_pairs(participants)
                return redirect("holiday:santa")
        elif action == "reset":
            participants.clear()
            pairs.clear()
            return redirect("holiday:santa")
        else:
            error = "Choose a valid action."

    context = {
        "form": form,
        "participants": participants,
        "pairs": pairs,
        "error": error,
    }
    return render(request, "holiday/santa.html", context)
