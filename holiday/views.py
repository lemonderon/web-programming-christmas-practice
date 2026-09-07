import random

from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ParticipantForm


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
    participants = request.session.get("participants", [])
    pairs = request.session.get("pairs", [])
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
                    # Reassign the key: Django does not detect nested list changes.
                    # https://docs.djangoproject.com/en/6.1/topics/http/sessions/#when-sessions-are-saved
                    request.session["participants"] = participants + [name]
                    request.session["pairs"] = []
                    return redirect("holiday:santa")
        elif action == "draw":
            if len(participants) < 2:
                error = "Add at least two participants before drawing."
            else:
                request.session["pairs"] = make_pairs(participants)
                return redirect("holiday:santa")
        elif action == "reset":
            request.session.pop("participants", None)
            request.session.pop("pairs", None)
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
