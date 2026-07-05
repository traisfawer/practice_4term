from django.core.management.base import BaseCommand

from restaurant.models import MenuItem, Speciality, StaticSection


class Command(BaseCommand):
    def handle(self, *args, **options):
        StaticSection.objects.all().delete()
        StaticSection.objects.create(
            key='about',
            title='About Us',
            subtitle='Ресторан авторской кухни.',
            text='Готовим блюда европейской и авторской кухни. '
                 'Работаем с 2015 года.',
        )
        StaticSection.objects.create(
            key='team',
            title='Master Chef',
            subtitle='Наш шеф-повар.',
            text='15 лет опыта в ресторанах Италии и Франции.',
        )
        StaticSection.objects.create(
            key='events',
            title='Private Events',
            subtitle='Проведём ваш вечер.',
            text='Дни рождения, свадьбы, корпоративы. Зал до 40 гостей.',
        )

        Speciality.objects.all().delete()
        Speciality.objects.create(order=0, title='Beef Wellington',
            subtitle='Signature', text='Говядина в тесте с грибами.')
        Speciality.objects.create(order=1, title='Truffle Risotto',
            subtitle='Main', text='Ризотто с пармезаном и трюфелем.')
        Speciality.objects.create(order=2, title='Seared Salmon',
            subtitle='Fish', text='Лосось на гриле.')

        MenuItem.objects.all().delete()
        items = [
            ('soup', 'Tomato Basil Soup', 'Томат, базилик', '7.90'),
            ('soup', 'French Onion', 'Луковый с грюйером', '8.50'),
            ('soup', 'Mushroom Cream', 'Крем-суп с грибами', '9.20'),
            ('soup', 'Chicken Broth', 'Chicken Broth', '6.80'),
            ('pizza', 'Margherita', 'Моцарелла, томаты', '11.00'),
            ('pizza', 'Prosciutto', 'Ветчина, руккола', '13.50'),
            ('pizza', 'Quattro Formaggi', 'Quattro Formaggi', '14.20'),
            ('pizza', 'Diavola', 'Пепперони', '12.80'),
            ('pizza', 'Vegetariana', 'Овощи', '11.90'),
            ('salad', 'Caesar', 'Курица, пармезан', '9.50'),
            ('salad', 'Greek', 'Фета, оливки', '8.90'),
            ('salad', 'Caprese', 'Моцарелла, песто', '10.20'),
            ('dessert', 'Tiramisu', 'Классический', '6.50'),
            ('dessert', 'Cheesecake', 'Нью-Йорк', '6.80'),
            ('dessert', 'Panna Cotta', 'С манго', '6.20'),
            ('dessert', 'Chocolate Fondant', 'С шоколадом', '7.90'),
            ('drinks', 'Espresso', '', '2.50'),
            ('drinks', 'Cappuccino', '', '3.20'),
            ('drinks', 'Fresh Orange', 'Свежевыжатый', '4.50'),
            ('drinks', 'House Lemonade', 'Мята, лайм', '4.00'),
            ('drinks', 'Sparkling Water', '', '3.00'),
        ]
        for cat, title, subtitle, price in items:
            MenuItem.objects.create(
                category=cat, title=title, subtitle=subtitle,
                price=price, on_main=True,
            )

        print('Done.')
