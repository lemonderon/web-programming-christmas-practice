from django.shortcuts import render
from django.utils import timezone


def is_christmas(request):
    today = timezone.localdate()
    context = {
        "today": today,
        "is_christmas": today.month == 12 and today.day == 25,
    }
    return render(request, "holiday/christmas.html", context)
