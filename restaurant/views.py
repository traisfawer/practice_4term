from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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

    text = 'From: %s <%s>\nPhone: %s\n\n%s' % (
        msg.name, msg.email, msg.phone or '-', msg.message,
    )
    send_mail('Contact message #%d' % msg.id, text,
              'noreply@hungry.local', ['office@hungry.local'],
              fail_silently=True)

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


@require_POST
def password_reset_request(request):
    email = request.POST.get('email', '').strip().lower()
    if not email:
        return JsonResponse({'ok': False, 'error': 'Введите email'}, status=400)

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return JsonResponse({'ok': True})

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = request.build_absolute_uri(
        reverse('password_reset_confirm', args=[uid, token])
    )
    send_mail(
        'Восстановление пароля',
        'Для сброса пароля перейдите по ссылке:\n\n' + link,
        'noreply@hungry.local',
        [user.email],
        fail_silently=True,
    )
    return JsonResponse({'ok': True})


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'restaurant/reset.html', {'invalid': True})

    if request.method == 'POST':
        password = request.POST.get('password', '')
        if len(password) < 6:
            return render(request, 'restaurant/reset.html', {
                'uidb64': uidb64, 'token': token,
                'error': 'Пароль минимум 6 символов',
            })
        user.set_password(password)
        user.save()
        return render(request, 'restaurant/reset.html', {'done': True})

    return render(request, 'restaurant/reset.html', {
        'uidb64': uidb64, 'token': token,
    })
