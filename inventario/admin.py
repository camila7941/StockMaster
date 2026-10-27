from django.contrib import admin
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_sku', 'nombre', 'categoria', 'precio_unitario', 'stock_actual', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre', 'codigo_sku')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'email', 'telefono')
    search_fields = ('nombre_completo', 'email')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'estado', 'total_acumulado')
    list_filter = ('estado', 'fecha_pedido')
    inlines = [DetallePedidoInline]


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'precio_historico', 'subtotal')