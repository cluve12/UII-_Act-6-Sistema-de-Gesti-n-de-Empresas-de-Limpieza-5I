from django.db import models

class Cliente_Limpieza(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=255)
    contacto_principal = models.CharField(max_length=100)
    email_contacto = models.EmailField(max_length=100, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    direccion_servicio = models.CharField(max_length=255, blank=True, null=True)
    tipo_negocio = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio_contrato = models.DateField(blank=True, null=True)
    estado_contrato = models.CharField(max_length=50, blank=True, null=True)
    frecuencia_servicio = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_empresa} ({self.contacto_principal})"


class Servicio_Limpieza(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    costo_estandar = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada_horas = models.IntegerField(blank=True, null=True)
    productos_usados = models.TextField(blank=True, null=True)
    requiere_equipo_especial = models.BooleanField(default=False)
    categoria_servicio = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre_servicio


class Empleado_Limpieza(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    fecha_contratacion = models.DateField(blank=True, null=True)
    salario_hora = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    turno = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    certificaciones_seguridad = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Programacion_Servicio(models.Model):
    id_programacion = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente_Limpieza,
        on_delete=models.CASCADE,
        related_name="programaciones"
    )
    servicio = models.ForeignKey(
        Servicio_Limpieza,
        on_delete=models.CASCADE,
        related_name="programaciones"
    )
    fecha_programada = models.DateTimeField()
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    estado_servicio = models.CharField(max_length=50, blank=True, null=True)
    observaciones_cliente = models.TextField(blank=True, null=True)
    empleado_asignado = models.ForeignKey(
        Empleado_Limpieza,
        on_delete=models.SET_NULL,
        related_name="programaciones_asignadas",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Prog {self.id_programacion} - {self.servicio} para {self.cliente}"


class Factura_Limpieza(models.Model):
    id_factura = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente_Limpieza,
        on_delete=models.CASCADE,
        related_name="facturas"
    )
    fecha_emision = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=50, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    programacion_asociada = models.ForeignKey(
        Programacion_Servicio,
        on_delete=models.SET_NULL,
        related_name="facturas",
        blank=True,
        null=True
    )
    impuestos_aplicados = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Factura {self.id_factura} - {self.cliente}"


class Material_Limpieza(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre_material = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    stock_actual = models.IntegerField(default=0)
    fecha_caducidad = models.DateField(blank=True, null=True)
    id_proveedor = models.IntegerField(blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_material = models.CharField(max_length=50, blank=True, null=True)
    ubicacion_almacen = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_material


class Uso_Material(models.Model):
    id_uso = models.AutoField(primary_key=True)
    programacion = models.ForeignKey(
        Programacion_Servicio,
        on_delete=models.CASCADE,
        related_name="usos_material"
    )
    material = models.ForeignKey(
        Material_Limpieza,
        on_delete=models.CASCADE,
        related_name="usos"
    )
    cantidad_usada = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    empleado_registro = models.ForeignKey(
        Empleado_Limpieza,
        on_delete=models.SET_NULL,
        related_name="usos_registrados",
        blank=True,
        null=True
    )
    comentarios_uso = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Uso {self.id_uso} - {self.material} ({self.cantidad_usada})"
