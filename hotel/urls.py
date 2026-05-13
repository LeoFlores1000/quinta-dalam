from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('contacto/', views.contacto, name='contacto'),
    path('reservar/', views.reservar, name='reservar'),
    path('mision/', views.mision, name='mision'),
    path('vision/', views.vision, name='vision'),
    path('panel/', views.panel_admin, name='panel_admin'),
    path(
        'disponibilidad/<int:habitacion_id>/',
        views.verificar_disponibilidad,
        name='disponibilidad'
    ),
    path(
        'buscar-habitaciones/',
        views.buscar_habitaciones,
        name='buscar_habitaciones'
    ),
    path(
        'crear-reservacion/',
        views.crear_reservacion,
        name='crear_reservacion'
    ),
    path(

        'cambiar-estado/',

        views.cambiar_estado_habitacion,

        name='cambiar_estado'

    ),
    path(

        'crear-habitacion/',

        views.crear_habitacion,

        name='crear_habitacion'

    ),
    path(

        'login/',

        views.login_view,

        name='login'
    ),
    path(

        'logout/',

        views.logout_view,

        name='logout'
    )

]