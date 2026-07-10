from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import BookingForm, ContactForm
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


@require_POST
def contact_create(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    msg = form.save()
    return JsonResponse({'ok': True, 'id': msg.id})


@require_POST
def register_view(request):
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')

    if not email or not password:
        return JsonResponse({'ok': False, 'error': 'Заполните email и пароль'}, status=400)
    if len(password) < 6:
        return JsonResponse({'ok': False, 'error': 'Пароль минимум 6 символов'}, status=400)
    if User.objects.filter(username=email).exists():
        return JsonResponse({'ok': False, 'error': 'Такой email уже зарегистрирован'}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    login(request, user)
    return JsonResponse({'ok': True, 'email': user.email})


@require_POST
def login_view(request):
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')

    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({'ok': False, 'error': 'Неверный email или пароль'}, status=400)

    login(request, user)
    return JsonResponse({'ok': True, 'email': user.email})


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'ok': True})
