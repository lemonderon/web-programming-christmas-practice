from django.http import HttpResponse
from django.utils import timezone


def is_christmas(request):
    today = timezone.localdate()
    answer = "Yes" if today.month == 12 and today.day == 25 else "No"
    return HttpResponse(answer)
