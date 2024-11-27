from django import forms
from .models import Caja, Pedido, Pago, Reserva, Compra, Mesa, Proveedor, Inventario, Categoria, DetalleCompra

# Formulario para Apertura de Caja
class AperturaCajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['total_inicial']

# Formulario para Cierre de Caja
class CierreCajaForm(forms.ModelForm):
    total_final = forms.DecimalField(max_digits=10, decimal_places=2)
    
    def clean_total_final(self):
        total_final = self.cleaned_data.get('total_final')
        if total_final <= 0:
            raise forms.ValidationError("El total final debe ser un valor positivo.")
        return total_final

    

    class Meta:
        model = Caja
        fields = ['total_final']



#pedido 
from django.forms import inlineformset_factory
from .models import Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'mesa', 'total', 'estado']  # O los campos que correspondan

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['menu', 'cantidad', 'precio_unitario']

# Creación del FormSet
PedidoFormSet = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1, can_delete=True)

class ModificarPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']




# Formulario para Pago
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago']

# Formulario para Modificar Pago
class ModificarPagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'monto']  # Incluye el campo para modificar el monto si es necesario


#from de reservas  
from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    fecha_reserva = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha y Hora de la Reserva'
    )

    class Meta:
        model = Reserva
        fields = ['mesa', 'fecha_reserva', 'nombre_cliente', 'telefono_cliente', 'estado', 'numero_personas', 'comentarios']

class ModificarReservaForm(forms.ModelForm):
    fecha_reserva = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Fecha y Hora de la Reserva'
    )

    class Meta:
        model = Reserva
        fields = ['mesa', 'fecha_reserva', 'nombre_cliente', 'telefono_cliente', 'estado', 'numero_personas', 'comentarios']

#cambia el estado de la reserva solamente
class CambiarEstadoReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [ 'estado']


# Formulario para Compra
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'total', 'tiene_documentacion', 'archivo_documentacion', 'detalle']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'tiene_documentacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'archivo_documentacion': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['inventario', 'cantidad', 'precio_unitario']
        widgets = {
            'inventario': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }    
        

# Formulario para Modificar Compra
class ModificarCompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'total']

# Formulario para Mesa
class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado']

# Formulario para Proveedor
from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'telefono', 'email', 'cuit', 'cbu', 'alias_cbu', 'calle', 'numero', 'localidad', 'pais', 'codigo_postal', 'plazo_pago', 'observaciones']
        labels = {
            'nombre_proveedor': 'Nombre del Proveedor',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'cuit': 'CUIT',
            'cbu': 'CBU',
            'alias_cbu': 'Alias CBU',
            'calle': 'Calle',
            'numero': 'N°',
            'localidad': 'Localidad',
            'pais': 'País',
            'codigo_postal': 'Código Postal',
            'plazo_pago': 'Plazo de Pago',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
            'cbu': forms.TextInput(attrs={'class': 'form-control'}),
            'alias_cbu': forms.TextInput(attrs={'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'plazo_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }


# Formulario para Inventario
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre_producto', 'cantidad_actual', 'cantidad_minima', 'unidad_medida']
        
        
        
        

# Fromulario de menu
from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nombre_plato', 'descripcion', 'precio', 'disponible', 'imagen', 'categoria']
        labels = {
            'nombre_plato': 'Nombre del Plato',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'disponible': 'Disponible',
            'imagen': 'Imagen del Plato',
            'categoria': 'Categoría',
        }
        widgets = {
            'nombre_plato': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        labels = {
            'nombre': 'Nombre de la Categoría',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        } 
#fin menu.       
        
        
        
        
        
        
        
        
        
#flujo de pedido por si tiene algun problema ver aca chicos.!

from .models import Pedido, DetallePedido
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['mesa', 'estado']  






from .models import DetallePedido, Menu

class DetallePedidoForm(forms.ModelForm):
    menu = forms.ModelChoiceField(
        queryset=Menu.objects.filter(disponible=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = DetallePedido
        fields = ['menu', 'cantidad', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio_unitario'].widget.attrs['class'] = 'form-control'
        
        

#Estadisticas
from .models import Usuario
class ReporteFiltroForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Desde')
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Hasta')
    usuario = forms.ModelChoiceField(
        queryset=Usuario.objects.filter(tipo_usuario__in=['admin', 'cajero']),
        required=False, label="Filtrar por Usuario"
    )
    

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, label="Tipo de Usuario")
    estado = forms.ChoiceField(choices=Usuario.ESTADO_CHOICES, label="Estado")

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'tipo_usuario', 'estado')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = self.cleaned_data['tipo_usuario']
        user.estado = self.cleaned_data['estado']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES, label="Tipo de Usuario")
    estado = forms.ChoiceField(choices=Usuario.ESTADO_CHOICES, label="Estado")

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'tipo_usuario', 'estado')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = self.cleaned_data['tipo_usuario']
        user.estado = self.cleaned_data['estado']
        if commit:
            user.save()
        return user
    
class CustomPasswordResetForm(forms.Form):
    nueva_contraseña = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirmar_contraseña = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if nueva_contraseña and confirmar_contraseña and nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
    

from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')
class CustomPasswordResetForm(forms.Form):
    nueva_contraseña = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirmar_contraseña = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
class CustomPasswordResetForm(forms.Form):
    nueva_contraseña = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirmar_contraseña = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if nueva_contraseña != confirmar_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
