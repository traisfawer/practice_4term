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

    if (typeof ymaps !== 'undefined' && $('#map').length) {
        ymaps.ready(function () {
            var map = new ymaps.Map('map', {
                center: [55.751574, 37.573856],
                zoom: 15,
                controls: ['zoomControl']
            });
            map.geoObjects.add(new ymaps.Placemark([55.751574, 37.573856], {
                balloonContent: 'Hungry People'
            }, {
                preset: 'islands#yellowFoodIcon'
            }));
        });
    }

});
