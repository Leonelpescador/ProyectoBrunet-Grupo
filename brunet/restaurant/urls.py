from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import CustomLoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    lista_mesas, 
    crear_mesa, 
    editar_mesa, 
    eliminar_mesa,
    crear_pedido, 
    modificar_pedido,
    eliminar_pedido,
    crear_pago,
    modificar_pago,
    eliminar_pago,
    crear_reserva,
    modificar_reserva,
    eliminar_reserva,
    proveedores, 
    editar_proveedor,
    eliminar_proveedor,
    crear_compra,  
    editar_compra,
    eliminar_compra,
    obtener_precio_plato,
    marcar_servido,
    crear_categoria, eliminar_categoria, listar_categorias, cocinero_dashboard, nuevos_pedidos, restablecer_contraseña,
   
)

urlpatterns =[
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Clientes
    path('cliente/', views.cliente, name='cliente'),
    
    
    #pedidos
    path('pedido/', views.pedidos_activos, name='pedidos_activos'),
    path('pedido/crear/<int:mesa_id>/', views.crear_pedido, name='crear_pedido'),
    path('pedido/modificar/<int:pedido_id>/', views.modificar_pedido, name='modificar_pedido'),
    path('pedido/eliminar/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('obtener_precio_plato/', obtener_precio_plato, name='obtener_precio_plato'),
    path('pedido/servido/<int:pedido_id>/', marcar_servido, name='marcar_servido'),
    path('cocina/nuevos_pedidos/', views.nuevos_pedidos, name='nuevos_pedidos'),
    path('cocina/pedidos_eliminados/', views.pedidos_eliminados, name='pedidos_eliminados'),



    # Pago 
    path('pago/crear/<int:pedido_id>/', views.crear_pago, name='crear_pago'),
    path('pago/modificar/<int:pago_id>/', views.modificar_pago, name='modificar_pago'),
    path('pago/eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
   

    # Reserva 
    path('reserva/crear/', views.crear_reserva, name='crear_reserva'),
    path('reserva/editar/<int:reserva_id>/', views.modificar_reserva, name='editar_reserva'),
    path('reserva/eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reserva/estado/<int:reserva_id>/', views.modificar_estado_reserva, name='modificar_estado_reserva'),
    path('reservas/', views.reservas, name='reservas'),


    # Inventario 
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/crear/', views.crear_inventario, name='crear_inventario'),
    path('inventario/editar/<int:pk>/', views.editar_inventario, name='editar_inventario'),
    path('inventario/eliminar/<int:pk>/', views.eliminar_inventario, name='eliminar_inventario'),
    path('inventario/descargar_plantilla/', views.descargar_plantilla_inventario, name='descargar_plantilla_inventario'),
    path('inventario/cargar/', views.cargar_inventario_masivo, name='cargar_inventario_masivo'),
    path('inventario/exportar/', views.exportar_inventario, name='exportar_inventario'),
    
    
    # Proveedor
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/cargar/', views.cargar_proveedores_masivo, name='cargar_proveedores_masivo'),
    path('proveedores/descargar-plantilla/', views.descargar_plantilla_proveedores, name='descargar_plantilla_proveedores'),
    
    
    # Compra 
    path('compra/', views.compras, name='compras'),
    path('compra/crear/', views.crear_compra, name='crear_compra'),  
    path('compra/editar/<int:pk>/', views.editar_compra, name='editar_compra'),
    path('compra/eliminar/<int:pk>/', views.eliminar_compra, name='eliminar_compra'),

    
    
    # Mesa 
    path('mesa/crear/', views.crear_mesa, name='crear_mesa'),
    path('mesa/', views.lista_mesas, name='lista_mesas'),
    path('mesa/eliminar/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),
    path('mesa/editar/<int:pk>/', views.editar_mesa, name='editar_mesa'),
    
    #estadisticas
    path('reportes/generar/', views.generar_reporte, name='generar_reporte'),
    path('reportes/grafico_ingresos/', views.obtener_datos_grafico_ingresos, name='obtener_datos_grafico_ingresos'),
    path('reportes/grafico_metodos_pago/', views.obtener_datos_grafico_metodos_pago, name='obtener_datos_grafico_metodos_pago'),
    
    
    # Caja 
    path('caja/apertura/', views.apertura_caja, name='apertura_caja'),
    path('caja/consulta/<int:caja_id>/', views.consulta_caja, name='consulta_caja'),
    path('caja/cierre/<int:caja_id>/', views.cierre_caja, name='cierre_caja'),
    path('caja/registrar_pago/<int:pedido_id>/', views.registrar_pago, name='registrar_pago'),
    path('caja/reporte/<int:caja_id>/', views.descargar_reporte_caja, name='descargar_reporte_caja'),
    
    # Menu "Platos"
    path('menu/listar/', views.listar_menu, name='listar_menu'),
    path('menu/crear/', views.crear_menu, name='crear_menu'),
    path('menu/editar/<int:menu_id>/', views.editar_menu, name='editar_menu'),
    path('menu/eliminar/<int:menu_id>/', views.eliminar_menu, name='eliminar_menu'),
    path('menu/cambiar-disponibilidad/<int:menu_id>/', views.cambiar_disponibilidad_menu, name='cambiar_disponibilidad_menu'),
    path('filtrar_platos_por_categoria/', views.filtrar_platos_por_categoria, name='filtrar_platos_por_categoria'),
    path('categoria/', listar_categorias, name='listar_categorias'),
    path('categoria/crear/', crear_categoria, name='crear_categoria'),
    path('categoria/eliminar/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    
    #cocina
    path('cocina/', cocinero_dashboard, name='cocinero_dashboard'),
    
    # Caja
    path('caja/pago/crear/', views.crear_pago, name='crear_pago'),
    path('caja/pago/modificar/<int:pago_id>/', views.modificar_pago, name='modificar_pago'),
    path('caja/pago/eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
    
    #Usuarios
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),  
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),  
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('usuario/restablecer_contraseña/<int:usuario_id>/', restablecer_contraseña, name='restablecer_contraseña'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
