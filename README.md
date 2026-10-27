# Tarea 1: Diseño del modelo de datos y creación de un proyecto web con Django

**Estudiante:** Maria Camila Rodriguez Ortiz 
**Institución:** Institución Universitaria Pascual Bravo  
**Asignatura:** Softgirls / Curso Django  

---

## 1. Identificación del Proyecto
* **Nombre de la Aplicación:** StockMaster 
* **Temática:** Sistema de Gestión de Inventarios y Pedidos para Emprendimientos.
* **Propósito:** Solución integral diseñada para automatizar el control de existencias, catalogar productos por categorías, administrar la base de datos de clientes y procesar transacciones comerciales mediante una arquitectura relacional sólida en Django.

---

## 2. Descripción de los Modelos de Datos (`models.py`)
El sistema cuenta con **5 entidades interconectadas** mediante relaciones de clave foránea (`ForeignKey`) que garantizan la integridad referencial de los datos:

1. **`Categoria`:** Agrupa los productos por líneas comerciales (ej. Electrónica, Accesorios).
2. **`Producto`:** Registra los artículos del inventario con su código SKU único, precio unitario y cantidad en stock actual. Posee una relación `1:N` con `Categoria` (`on_delete=models.PROTECT`).
3. **`Cliente`:** Mantiene la información de contacto y dirección de los compradores.
4. **`Pedido`:** Representa el encabezado de la venta asociado a un cliente (`1:N` con `Cliente`) con su estado operativo y fecha de registro.
5. **`DetallePedido`:** Tabla intermedia que resuelve la relación `N:M` entre `Pedido` y `Producto`. Registra cantidades y almacena el `precio_historico` de cada artículo para proteger las auditorías financieras ante futuros cambios de precio en el catálogo.

---

