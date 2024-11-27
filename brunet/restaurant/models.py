from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Admin'),
        ('cajero', 'Cajero'),
        ('mesero', 'Mesero'),
        ('cocinero', 'Cocinero'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    ultima_sesion = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Mesa(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]
    numero_mesa = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        return f'Mesa {self.numero_mesa}'

# Definición del modelo Menu
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Menu(models.Model):
    nombre_plato = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='menus')  

    def __str__(self):
        return self.nombre_plato

    
    
    
from django.utils import timezone

from django.db import models
from django.conf import settings

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('servido', 'Servido'),
        ('pagado', 'Pagado'),
        ('eliminado', 'Eliminado'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mesa = models.ForeignKey('Mesa', on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    en_proceso = models.BooleanField(default=False)
    usuario_procesando = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_en_proceso'
    )
    numero_comanda = models.PositiveIntegerField(unique=True, null=True, blank=True)

    def marcar_en_proceso(self, usuario):
        self.en_proceso = True
        self.usuario_procesando = usuario
        self.save()

    def marcar_completado(self):
        self.estado = 'servido'
        self.save()

    def save(self, *args, **kwargs):
        if not self.numero_comanda:
            # Obtener el último pedido con numero_comanda asignado
            last_pedido = Pedido.objects.exclude(numero_comanda__isnull=True).order_by('numero_comanda').last()

            if last_pedido:
                self.numero_comanda = last_pedido.numero_comanda + 1
            else:
                self.numero_comanda = 1  # Si no existe ningún pedido con comanda, empezar con 1

        super(Pedido, self).save(*args, **kwargs)

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.mesa.numero_mesa} - Estado {self.estado}'




class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)  
    subtotal = models.DecimalField(max_digits=14, decimal_places=2)  

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.menu.nombre_plato} - {self.cantidad} unidades'



from django.db import models
from .models import Usuario, Mesa

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()
    nombre_cliente = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=15, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    
    numero_personas = models.IntegerField()

    
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva para {self.nombre_cliente} en {self.mesa} - {self.fecha_reserva.strftime('%d/%m/%Y %H:%M')} - {self.estado}"


class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia')])
    comprobante = models.FileField(upload_to='comprobantes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        
        self.monto = self.pedido.total
        
        
        super().save(*args, **kwargs)
        
        
        self.pedido.refresh_from_db()

        
        print(f"Estado actual del pedido: {self.pedido.estado}")  #
        if self.pedido.estado == 'servido':
            print(f"Pedido {self.pedido.id} está servido. Cambiando estado a pagado...")
            
            try:
                self.pedido.estado = 'pagado'
                self.pedido.save()  
                print(f"Estado del pedido {self.pedido.id} ha sido actualizado a pagado.")
            except Exception as e:
                print(f"Error al actualizar el estado del pedido: {e}")
        else:
            print(f"Pedido {self.pedido.id} no está en estado 'servido'. Estado actual: {self.pedido.estado}")





class Inventario(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('KG', 'Kilogramos'),
        ('G', 'Gramos'),
        ('L', 'Litros'),
        ('Ud', 'Unidad'),
    ]

    nombre_producto = models.CharField(max_length=100)
    cantidad_actual = models.IntegerField()
    cantidad_minima = models.IntegerField()
    unidad_medida = models.CharField(
        max_length=2,
        choices=UNIDAD_MEDIDA_CHOICES,
        default='Ud'
    )

    def __str__(self):
        return f'{self.nombre_producto} ({self.unidad_medida})'



class Proveedor(models.Model):
    codigo = models.PositiveIntegerField(unique=True, editable=False)
    nombre_proveedor = models.CharField(max_length=255)
    cuit = models.CharField(max_length=15, blank=True, null=True)
    cbu = models.CharField(max_length=22, blank=True, null=True)
    alias_cbu = models.CharField(max_length=100, blank=True, null=True)
    calle = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    plazo_pago = models.PositiveIntegerField(blank=True, null=True, help_text="Plazo de pago en días.")
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre_proveedor}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            last_proveedor = Proveedor.objects.all().order_by('codigo').last()
            if last_proveedor:
                self.codigo = last_proveedor.codigo + 1
            else:
                self.codigo = 1
        super(Proveedor, self).save(*args, **kwargs)


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tiene_documentacion = models.BooleanField(default=False)
    archivo_documentacion = models.FileField(upload_to='documentos/', blank=True, null=True)
    detalle = models.TextField(blank=True, null=True)
    fecha_compra = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.proveedor.nombre_proveedor} por ${self.total}"
    
    
class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

from django.db import models
from django.utils import timezone
from restaurant.models import Pago

class Caja(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    apertura = models.DateTimeField(auto_now_add=True)
    cierre = models.DateTimeField(blank=True, null=True)
    total_inicial = models.DecimalField(max_digits=12, decimal_places=2)
    total_final = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=10, default='abierta')

    def cerrar_caja(self, total_final):
        self.cierre = timezone.now()
        self.total_final = total_final
        self.estado = 'cerrada'
        self.save()

    def calcular_total_final(self):
        total_ingresos = sum(transaccion.monto for transaccion in self.transacciones.filter(tipo='ingreso'))
        return self.total_inicial + total_ingresos

    def __str__(self):
        return f'Caja {self.id} - {self.usuario.username}'

class TransaccionCaja(models.Model):
    caja = models.ForeignKey(Caja, related_name='transacciones', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')])
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    pago = models.ForeignKey(Pago, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return f'Transacción {self.tipo} - {self.monto}'
