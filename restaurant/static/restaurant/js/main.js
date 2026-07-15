$(function () {

    var nav = $('#mainNav');

    $(window).on('scroll', function () {
        if ($(window).scrollTop() > 40) {
            nav.addClass('is-sticky');
        } else {
            nav.removeClass('is-sticky');
        }
    });

    $('a[href^="#"]').on('click', function (e) {
        var href = $(this).attr('href');
        if (href === '#') return;
        var target = $(href);
        if (!target.length) return;
        e.preventDefault();
        var offset = nav.outerHeight() || 0;
        $('html, body').animate({ scrollTop: target.offset().top - offset }, 450);
    });

    $('.specialities__slider').slick({
        arrows: false,
        dots: true,
        infinite: true,
        speed: 500,
        fade: true,
        autoplay: false
    });

    $('#bookingForm').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        var msg = $('#bookingMessage');
        msg.removeClass('is-ok is-error').text('Отправка...');

        $.ajax({
            url: '/api/booking/',
            method: 'POST',
            data: form.serialize(),
            success: function (data) {
                if (data.ok) {
                    msg.addClass('is-ok').text('Спасибо! Бронь #' + data.id);
                    form[0].reset();
                } else {
                    msg.addClass('is-error').text('Проверьте поля');
                }
            },
            error: function () {
                msg.addClass('is-error').text('Ошибка отправки');
            }
        });
    });

    $('#contactForm').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        var msg = $('#contactMessage');
        msg.removeClass('is-ok is-error').text('Отправка...');

        $.ajax({
            url: '/api/contact/',
            method: 'POST',
            data: form.serialize(),
            success: function (data) {
                if (data.ok) {
                    msg.addClass('is-ok').text('Сообщение отправлено, спасибо!');
                    form[0].reset();
                } else {
                    msg.addClass('is-error').text('Проверьте поля');
                }
            },
            error: function () {
                msg.addClass('is-error').text('Ошибка отправки');
            }
        });
    });

    var items = $('#menuList .menu__item');

    $('.menu__filter').on('click', function () {
        var cat = $(this).data('cat');
        $('.menu__filter').removeClass('menu__filter--active');
        $(this).addClass('menu__filter--active');

        var arr = items.toArray();
        var visible = cat === 'all' ? arr : arr.filter(function (el) {
            return $(el).data('category') === cat;
        });

        items.hide();
        $(visible).show();
    });

    function showAuthTab(tab) {
        $('.auth__tab').removeClass('auth__tab--active');
        $('#loginForm, #registerForm, #resetForm').hide();
        if (tab === 'login') {
            $('.auth__tab[data-tab="login"]').addClass('auth__tab--active');
            $('#loginForm').show();
        } else if (tab === 'register') {
            $('.auth__tab[data-tab="register"]').addClass('auth__tab--active');
            $('#registerForm').show();
        } else {
            $('#resetForm').show();
        }
    }

    $('.auth__tab').on('click', function () {
        showAuthTab($(this).data('tab'));
    });

    $('#forgotLink').on('click', function (e) {
        e.preventDefault();
        showAuthTab('reset');
    });

    $('#backToLoginLink').on('click', function (e) {
        e.preventDefault();
        showAuthTab('login');
    });

    $('#resetForm').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        var msg = $('#resetMessage');
        msg.removeClass('is-ok is-error').text('Отправка...');

        $.ajax({
            url: '/api/reset/',
            method: 'POST',
            data: form.serialize(),
            success: function () {
                msg.addClass('is-ok').text('Если email зарегистрирован, ссылка отправлена на почту.');
                form[0].reset();
            },
            error: function (xhr) {
                var err = (xhr.responseJSON && xhr.responseJSON.error) || 'Ошибка';
                msg.addClass('is-error').text(err);
            }
        });
    });

    $('#loginForm').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        var msg = $('#loginMessage');
        msg.removeClass('is-ok is-error').text('Отправка...');

        $.ajax({
            url: '/api/login/',
            method: 'POST',
            data: form.serialize(),
            success: function () {
                msg.addClass('is-ok').text('Вход выполнен');
                setTimeout(function () { location.reload(); }, 600);
            },
            error: function (xhr) {
                var err = (xhr.responseJSON && xhr.responseJSON.error) || 'Ошибка входа';
                msg.addClass('is-error').text(err);
            }
        });
    });

    $('#registerForm').on('submit', function (e) {
        e.preventDefault();
        var form = $(this);
        var msg = $('#registerMessage');
        msg.removeClass('is-ok is-error').text('Отправка...');

        $.ajax({
            url: '/api/register/',
            method: 'POST',
            data: form.serialize(),
            success: function () {
                msg.addClass('is-ok').text('Регистрация успешна');
                setTimeout(function () { location.reload(); }, 600);
            },
            error: function (xhr) {
                var err = (xhr.responseJSON && xhr.responseJSON.error) || 'Ошибка регистрации';
                msg.addClass('is-error').text(err);
            }
        });
    });

    $('#logoutLink').on('click', function (e) {
        e.preventDefault();
        var token = $('input[name=csrfmiddlewaretoken]').first().val();
        $.ajax({
            url: '/api/logout/',
            method: 'POST',
            data: { csrfmiddlewaretoken: token },
            complete: function () { location.reload(); }
        });
    });

    if (typeof ymaps !== 'undefined' && $('#map').length) {
        ymaps.ready(function () {
            var map = new ymaps.Map('map', {
                center: [55.751574, 37.573856],
                zoom: 15,
                controls: ['zoomControl', 'routeButtonControl', 'typeSelector', 'fullscreenControl']
            });
            map.geoObjects.add(new ymaps.Placemark([55.751574, 37.573856], {
                balloonContent: 'Hungry People',
                hintContent: 'Наш ресторан'
            }, {
                preset: 'islands#yellowFoodIcon'
            }));

            var routeBtn = map.controls.get('routeButtonControl');
            if (routeBtn) {
                routeBtn.routePanel.state.set({
                    type: 'auto',
                    toEnabled: false,
                    to: 'Москва, ул. Ресторанная, 10'
                });
            }
        });
    }

});
