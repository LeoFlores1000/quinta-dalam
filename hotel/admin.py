from django.contrib import admin
from .models import Habitacion, ImagenHabitacion
from .models import Reservacion


class ImagenHabitacionInline(admin.TabularInline):
    model = ImagenHabitacion
    extra = 1


class HabitacionAdmin(admin.ModelAdmin):
    inlines = [ImagenHabitacionInline]

from .models import (
    Habitacion,
    Reservacion,
    ImagenHabitacion,
    MensajeContacto
)

admin.site.register(Habitacion, HabitacionAdmin)
admin.site.register(Reservacion)
admin.site.register(ImagenHabitacion)
admin.site.register(MensajeContacto)