from hotel.models import Habitacion, ImagenHabitacion


Habitacion.objects.all().delete()


habitaciones_data = [
    {
        "nombre": "Suite Tzintzuntzan",
        "tag": "suite",
        "precio": 1500,
        "descripcion": "Inspirada en el tradicional pueblo de Tzintzuntzan. Un espacio amplio lleno de luz natural y artesanía local.",
        "amenities": "Cama King Size,Balcón con vista,Máquina de café",
        "imagenes": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAdG2CazjXjZk75x1liXktIy40R9GbzRzvNg&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSzPLWCQCoMir3czXdjxmJV-1qoAbtuyrF8GA&s",
            "https://upload.wikimedia.org/wikipedia/commons/1/16/Tzintzuntzan.jpg"
        ]
    },

    {
        "nombre": "Dormitorio Morelia",
        "tag": "presidencial",
        "precio": 2200,
        "descripcion": "El lujo de la época colonial. Muros de piedra tallada, techos altos y una atmósfera romántica.",
        "amenities": "Jacuzzi Privado,Chimenea artesanal,Minibar incluido",
        "imagenes": [
            "https://etn.com.mx/blog/wp-content/uploads/2024/03/istockphoto-1222700177-612x612-1.jpg",
            "https://www.infobae.com/new-resizer/0jTVTrSUVwaEpbhP9fVQHYiu3B4=/arc-anglerfish-arc2-prod-infobae/public/VB3QWTD6SBCYXPZSXDVBFQRUYM.jpeg",
            "https://cbamericas.com.mx/wp-content/uploads/2024/08/Morelia-se-recupera-en-materia-turistica.jpg"
        ]
    },

    {
        "nombre": "Cabana Zirahuen",
        "tag": "cabana",
        "precio": 1800,
        "descripcion": "Privacidad total apartada del edificio principal con acabados en madera fina.",
        "amenities": "Terraza privada,Cama Queen Size,Fogatero exterior",
        "imagenes": [
            "https://assets.visitmichoacan.com.mx/images/experiences/lago-de-zirahuen/lago-de-zirahuen-gallery-02-soyxfr.jpg",
            "https://visitmexico.com/media/usercontent/680a57476451c-Captura-de-pantalla-2025-04-24-092038_gmxdot_png",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1VKdNESe01dE891hcWDlIdzzuMROaQbIwIA&s"
        ]
    },
]


for data in habitaciones_data:

    imagenes = data.pop('imagenes')

    habitacion = Habitacion.objects.create(**data)

    for url in imagenes:
        ImagenHabitacion.objects.create(
            habitacion=habitacion,
            imagen=url
        )


print('Habitaciones cargadas correctamente 😎🔥')