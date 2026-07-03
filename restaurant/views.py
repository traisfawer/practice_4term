from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import MenuItem, Speciality, StaticSection


def index(request):
    about = StaticSection.objects.filter(key='about').first()
    team = StaticSection.objects.filter(key='team').first()
    events = StaticSection.objects.filter(key='events').first()

    context = {
        'about': about,
        'team': team,
        'events': events,
        'specialities': Speciality.objects.all(),
        'menu_items': MenuItem.objects.filter(on_main=True)[:21],
        'menu_categories': MenuItem.CATEGORY_CHOICES,
    }
    return render(request, 'restaurant/index.html', context)


@require_POST
def booking_create(request):
    form = BookingForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    booking = form.save()

    text = 'Booking #%d\n%s, %s, %s\n%s %s' % (
        booking.id, booking.name, booking.email, booking.phone,
        booking.date, booking.time,
    )
    send_mail('Booking #%d' % booking.id, text,
              'noreply@hungry.local', [booking.email],
              fail_silently=True)

    return JsonResponse({'ok': True, 'id': booking.id})
