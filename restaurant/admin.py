from django.contrib import admin

from .models import Booking, ContactMessage, MenuItem, Speciality, StaticSection

admin.site.register(StaticSection)
admin.site.register(Speciality)
admin.site.register(MenuItem)
admin.site.register(Booking)
admin.site.register(ContactMessage)
