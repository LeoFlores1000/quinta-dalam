from django.db import models


class Habitacion(models.Model):

    TAGS = [
        ('suite', 'Suite Premium'),
        ('presidencial', 'Suite Presidencial'),
        ('cabana', 'Cabaña Ecológica'),
        ('estandar', 'Habitación Estándar'),
    ]

    nombre = models.CharField(max_length=100)

    tag = models.CharField(
        max_length=30,
        choices=TAGS
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descripcion = models.TextField()

    amenities = models.TextField(
        help_text="Separadas por comas"
    )

    disponible = models.BooleanField(default=True)

    def amenities_lista(self):
        return self.amenities.split(',')

    def primera_imagen(self):
        primera = self.imagenes.first()
        return primera.imagen if primera else ''

    def __str__(self):
        return self.nombre

    ESTADOS = [

        ('libre', 'Libre'),

        ('limpieza', 'Limpieza')
    ]

    estado = models.CharField(

        max_length=20,

        choices=ESTADOS,

        default='libre'

    )

class ImagenHabitacion(models.Model):

    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )

    imagen = models.URLField()

    def __str__(self):
        return f"Imagen de {self.habitacion.nombre}"

class Reservacion(models.Model):

    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.CASCADE,
        related_name='reservaciones'
    )

    nombre_cliente = models.CharField(max_length=100)

    email = models.EmailField()

    telefono = models.CharField(max_length=20)

    check_in = models.DateField()

    check_out = models.DateField()

    huespedes = models.IntegerField()

    fecha_reserva = models.DateTimeField(auto_now_add=True)

    apellidos = models.CharField(
    max_length=100
    )

    motivo = models.CharField(
        max_length=100,
        blank=True
    )

    hora_llegada = models.CharField(
        max_length=50,
        blank=True
    )

    peticiones = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.nombre_cliente} - {self.habitacion.nombre}"  
    
class MensajeContacto(models.Model):

    nombre = models.CharField(max_length=100)

    correo = models.EmailField()

    asunto = models.CharField(max_length=200)

    mensaje = models.TextField()

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    respondido = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.nombre