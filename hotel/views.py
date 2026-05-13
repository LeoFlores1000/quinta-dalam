from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import (

    Habitacion,

    Reservacion,

    ImagenHabitacion,

    MensajeContacto

)

import json


def home(request):
    return render(request, 'index.html')

def mision(request):
    return render(request, 'mision.html')

def vision(request):
    return render(request, 'vision.html')

def catalogo(request):

    habitaciones = Habitacion.objects.all()

    return render(request, 'catalogo.html', {
        'habitaciones': habitaciones
    })

def contacto(request):

    if request.method == 'POST':

        nombre = request.POST.get('nombre')

        correo = request.POST.get('correo')

        asunto = request.POST.get('asunto')

        mensaje = request.POST.get('mensaje')

        MensajeContacto.objects.create(

            nombre=nombre,

            correo=correo,

            asunto=asunto,

            mensaje=mensaje

        )

        return JsonResponse({
            'success': True
        })

    return render(
        request,
        'contacto.html'
    )

def reservar(request):

    check_in = request.GET.get('in')

    check_out = request.GET.get('out')

    huespedes = request.GET.get('g')

    habitaciones_disponibles = []

    if check_in and check_out:

        check_in_date = datetime.strptime(

            check_in,

            '%Y-%m-%d'

        ).date()

        check_out_date = datetime.strptime(

            check_out,

            '%Y-%m-%d'

        ).date()

        habitaciones = Habitacion.objects.all()

        for habitacion in habitaciones:

            conflicto = Reservacion.objects.filter(

                habitacion=habitacion,

                check_in__lt=check_out_date,

                check_out__gt=check_in_date

            ).exists()

            if not conflicto:

                habitaciones_disponibles.append(

                    habitacion

                )

    return render(request, 'reservar.html', {

        'habitaciones': habitaciones_disponibles,

        'check_in': check_in,

        'check_out': check_out,

        'huespedes': huespedes

    })

@login_required(login_url='/login/')
def panel_admin(request):

    hoy = timezone.now().date()

    total_habitaciones = Habitacion.objects.count()

    ocupadas = Reservacion.objects.filter(

        check_in__lte=hoy,

        check_out__gte=hoy

    ).count()

    porcentaje_ocupacion = 0

    if total_habitaciones > 0:

        porcentaje_ocupacion = int(

            (ocupadas / total_habitaciones) * 100

        )

    checkins_hoy = Reservacion.objects.filter(

        check_in=hoy

    ).count()

    ingresos = Reservacion.objects.all().aggregate(

        total=Sum('habitacion__precio')

    )['total'] or 0

    habitaciones = Habitacion.objects.all()

    habitaciones_estado = []

    for habitacion in habitaciones:

        print("========")

        print("Habitación:", habitacion.nombre)

        reserva_activa = Reservacion.objects.filter(

            habitacion=habitacion,

            check_in__lte=hoy,

            check_out__gte=hoy

        ).first()

        print("Reserva encontrada:", reserva_activa)

        estado = 'libre'

        if reserva_activa:

            estado = 'ocupada'

        elif habitacion.estado == 'limpieza':

            estado = 'limpieza'

        habitaciones_estado.append({

            'habitacion': habitacion,

            'estado': estado,

            'reserva': reserva_activa

        })

    reservaciones_recientes = Reservacion.objects.filter(

        check_in__lte=hoy,

        check_out__gte=hoy

    ).select_related('habitacion')

    return render(request, 'admin.html', {

        'habitaciones_estado': habitaciones_estado,

        'reservaciones_recientes': reservaciones_recientes,

        'ingresos': ingresos,

        'ocupacion': porcentaje_ocupacion,

        'checkins_hoy': checkins_hoy,

    })

def verificar_disponibilidad(request, habitacion_id):


    habitacion = get_object_or_404(
        Habitacion,
        id=habitacion_id
    )

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if not check_in or not check_out:

        return JsonResponse({
            'error': 'Fechas incompletas'
        }, status=400)

    check_in = datetime.strptime(
        check_in,
        '%Y-%m-%d'
    ).date()

    check_out = datetime.strptime(
        check_out,
        '%Y-%m-%d'
    ).date()


    reservas = Reservacion.objects.all()

    for r in reservas:
        print(
            r.habitacion.id,
            r.habitacion.nombre,
            r.check_in,
            r.check_out
    )

    conflicto = Reservacion.objects.filter(
        habitacion=habitacion
    ).filter(
        check_in__lt=check_out,
        check_out__gt=check_in
    ).exists()

    print("¿Hay conflicto?", conflicto)

    return JsonResponse({
        'disponible': not conflicto
    })

def buscar_habitaciones(request):

    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if not check_in or not check_out:
        return JsonResponse([], safe=False)

    check_in_date = datetime.strptime(
        check_in,
        '%Y-%m-%d'
    ).date()

    check_out_date = datetime.strptime(
        check_out,
        '%Y-%m-%d'
    ).date()

    habitaciones_disponibles = []

    habitaciones = Habitacion.objects.all()

    for habitacion in habitaciones:

        conflicto = Reservacion.objects.filter(
            habitacion=habitacion,
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        ).exists()

        if not conflicto:

            habitaciones_disponibles.append({
                'id': habitacion.id,
                'nombre': habitacion.nombre,
                'tag': habitacion.get_tag_display(),
                'precio': float(habitacion.precio),
                'descripcion': habitacion.descripcion,
                'imagen': habitacion.primera_imagen(),
                'amenities': habitacion.amenities_lista(),
            })

    return JsonResponse(
        habitaciones_disponibles,
        safe=False
    )

@csrf_exempt
def crear_reservacion(request):

    if request.method != 'POST':

        return JsonResponse({
            'error': 'Método inválido'
        }, status=400)

    data = json.loads(request.body)

    habitacion = Habitacion.objects.get(
        id=data['habitacion_id']
    )

    check_in = datetime.strptime(
        data['check_in'],
        '%Y-%m-%d'
    ).date()

    check_out = datetime.strptime(
        data['check_out'],
        '%Y-%m-%d'
    ).date()

    conflicto = Reservacion.objects.filter(
        habitacion=habitacion,
        check_in__lt=check_out,
        check_out__gt=check_in
    ).exists()

    if conflicto:

        return JsonResponse({
            'error': 'La habitación ya no está disponible'
        }, status=409)

    Reservacion.objects.create(

        habitacion=habitacion,

        nombre_cliente=data['nombre'],

        apellidos=data['apellidos'],

        email=data['email'],

        telefono=data['telefono'],

        check_in=check_in,

        check_out=check_out,

        huespedes=data['huespedes'],

        motivo=data.get('motivo', ''),

        hora_llegada=data.get('hora_llegada', ''),

        peticiones=data.get('peticiones', '')

    )

    return JsonResponse({
        'success': True
    })

@csrf_exempt
def cambiar_estado_habitacion(request):

    if request.method != 'POST':

        return JsonResponse({

            'error': 'Método inválido'

        }, status=400)

    data = json.loads(request.body)

    habitacion = Habitacion.objects.get(

        id=data['habitacion_id']

    )

    habitacion.estado = data['estado']

    habitacion.save()

    return JsonResponse({

        'success': True

    })

@csrf_exempt
def crear_habitacion(request):

    if request.method != 'POST':

        return JsonResponse({

            'error': 'Método inválido'

        }, status=400)

    data = json.loads(request.body)

    habitacion = Habitacion.objects.create(

        nombre=data['nombre'],

        tag=data['tag'],

        precio=data['precio'],

        descripcion=data['descripcion'],

        amenities=data['amenities']

    )

    imagenes = data['imagenes']

    for img in imagenes:

        if img.strip() != '':

            ImagenHabitacion.objects.create(

                habitacion=habitacion,

                imagen=img.strip()

            )

    return JsonResponse({

        'success': True

    })

def login_view(request):


    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None:

            login(request, user)

            return redirect('panel_admin')

    return render(request, 'login.html')

def logout_view(request):

    logout(request)

    return redirect('logout')