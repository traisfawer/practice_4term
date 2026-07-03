from django.db import models


class StaticSection(models.Model):
    KEY_CHOICES = [
        ('about', 'About Us'),
        ('team', 'Our Team'),
        ('events', 'Private Events'),
    ]
    key = models.CharField(max_length=20, choices=KEY_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='static_sections/', blank=True, null=True)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='specialities/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('soup', 'Soupe'),
        ('pizza', 'Pizza'),
        ('salad', 'Salad'),
        ('dessert', 'Dessert'),
        ('drinks', 'Drinks'),
    ]
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    on_main = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    people = models.PositiveSmallIntegerField()
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
