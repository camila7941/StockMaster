from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        related_name='productos',
        verbose_name="Categoría"
    )
    codigo_sku = models.CharField(max_length=50, unique=True, verbose_name="Código SKU")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario ($)")
    stock_actual = models.PositiveIntegerField(default=0, verbose_name="Stock Actual")
    activo = models.BooleanField(default=True, verbose_name="Disponible para Venta")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"[{self.codigo_sku}] {self.nombre} - ${self.precio_unitario}"


class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección de Envío")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre_completo']

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'En Proceso'),
        ('ENVIADO', 'Enviado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='pedidos',
        verbose_name="Cliente"
    )
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    estado = models.CharField(
        max_length=15, 
        choices=ESTADO_CHOICES, 
        default='PENDIENTE', 
        verbose_name="Estado del Pedido"
    )
    total_acumulado = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Total Acumulado ($)"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} | Cliente: {self.cliente.nombre_completo} | Estado: {self.get_estado_display()}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='detalles',
        verbose_name="Pedido"
    )
    producto = models.ForeignKey(
        Producto, 
        on_delete=models.PROTECT, 
        related_name='detalles_pedido',
        verbose_name="Producto"
    )
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_historico = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Precio al comprar ($)"
    )
    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        editable=False, 
        verbose_name="Subtotal ($)"
    )

    class Meta:
        verbose_name = "Detalle del Pedido"
        verbose_name_plural = "Detalles de Pedidos"

    def save(self, *args, **kwargs):
        if not self.precio_historico and self.producto:
            self.precio_historico = self.producto.precio_unitario
        self.subtotal = self.cantidad * self.precio_historico
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido #{self.pedido.id} -> {self.cantidad}x {self.producto.nombre} (${self.subtotal})"
# Create your models here.
