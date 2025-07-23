from django.db import models

class usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena_usuario = models.CharField(max_length=100)



class Login(models.Model):
    id_login = models.AutoField(primary_key=True)
    nombre_login = models.CharField(max_length=100, unique=True)
    contrasena_login = models.CharField(max_length=100)



class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="clientes")
    nombre_cliente = models.CharField(max_length=100)
    direccion_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=20)
    correo_cliente = models.EmailField()
    fecha_registro_cliente = models.DateTimeField(auto_now_add=True)


class Tecnico(models.Model):
    id_tecnico = models.AutoField(primary_key=True)
    id_login = models.ForeignKey(Login, on_delete=models.CASCADE, related_name="tecnicos")
    nombre_tecnico = models.CharField(max_length=100)
    especialidad_tecnico = models.CharField(max_length=100)
    telefono_tecnico = models.CharField(max_length=20)
    correo_tecnico = models.EmailField()
    fecha_contratacion_tecnico = models.DateField()



class Electrodomestico(models.Model):
    id_electrodomestico = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="electrodomesticos")
    tipo_electrodomestico = models.CharField(max_length=100)
    marca_electrodomestico = models.CharField(max_length=100)
    modelo_electrodomestico = models.CharField(max_length=100)
    descripcion_falla_electrodomestico = models.TextField()
    fecha_ingreso_electrodomestico = models.DateField()


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    id_tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name="servicios")
    id_electrodomestico = models.ForeignKey(Electrodomestico, on_delete=models.CASCADE, related_name="servicios")
    descripcion_servicio_servicio = models.TextField()
    costo_estimado_servicio = models.DecimalField(max_digits=8, decimal_places=2)
    estado_servicio = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Finalizado', 'Finalizado')])
    fecha_inicio_servicio = models.DateField()
    fecha_fin_servicio = models.DateField(null=True, blank=True)


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="facturas")
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="facturas")
    fecha_emision_factura = models.DateField(auto_now_add=True)
    monto_total_factura = models.DecimalField(max_digits=8, decimal_places=2)
    pagado_factura = models.CharField(max_length=50, choices=[('Si', 'Si'), ('No', 'No')])
    estado_factura = models.CharField(max_length=50, choices=[('Vigente', 'Vigente'), ('Expirada', 'Expirada')])
    tiempo_factura = models.IntegerField()



