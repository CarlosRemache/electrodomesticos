from django.shortcuts import render, redirect
from .models import Login, Cliente, Tecnico, Electrodomestico,Servicio,Factura,usuario
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from datetime import timedelta
from django.contrib import messages
from django.db.models.functions import ExtractYear
import json



# -------------- Login --------------------

def login_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena_usuario')

        try:
            user = usuario.objects.get(nombre_usuario=nombre, contrasena_usuario=contrasena)
            request.session['usuario_id'] = user.id_usuario
            request.session['usuario_nombre'] = user.nombre_usuario
            return redirect('menu')
        except usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')


def menu_view(request):
    if 'usuario_id' not in request.session:
        return redirect('login')
    nombre = request.session.get('usuario_nombre')
    return render(request, 'inicio.html', {'nombre': nombre})


def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')







# ------------------------------- Graficos y estadísticas -------------------------------

def inicio(request):
    # Gráfico1
    grafico1_labels = []
    grafico1_data = []

    servicios = Servicio.objects.values('descripcion_servicio_servicio', 'costo_estimado_servicio')\
                .order_by('-costo_estimado_servicio')[:5]

    for s in servicios:
        grafico1_labels.append(s['descripcion_servicio_servicio'])
        grafico1_data.append(float(s['costo_estimado_servicio']))


  # Gráfico 2 
    grafico2_labels = []
    grafico2_data = []
    tecnicos = Tecnico.objects.values('especialidad_tecnico')\
                .annotate(cantidad=Count('id_tecnico'))\
                .order_by('-cantidad')

    for t in tecnicos:
        grafico2_labels.append(t['especialidad_tecnico'])
        grafico2_data.append(t['cantidad'])

  # Gráfico 3 - Conteo de servicios por tipo de electrodoméstico
    grafico3_labels = []
    grafico3_data = []

    servicios_por_tipo = Servicio.objects.values('id_electrodomestico__tipo_electrodomestico')\
        .annotate(total_servicios=Count('id_servicio'))\
        .order_by('id_electrodomestico__tipo_electrodomestico')

    for item in servicios_por_tipo:
        grafico3_labels.append(item['id_electrodomestico__tipo_electrodomestico'])
        grafico3_data.append(item['total_servicios'])


    # Gráfico 4 
    grafico4_labels = []
    grafico4_data = []

    estados = Servicio.objects.values('estado_servicio')\
        .annotate(total=Count('id_servicio'))\
        .order_by('estado_servicio')

    for item in estados:
        grafico4_labels.append(item['estado_servicio'])
        grafico4_data.append(item['total'])

    # Gráfico 5 
    grafico5_labels = []
    grafico5_data = []

    marcas = Electrodomestico.objects.values('marca_electrodomestico')\
        .annotate(total=Count('id_electrodomestico'))\
        .order_by('-total')

    for item in marcas:
        grafico5_labels.append(item['marca_electrodomestico'])
        grafico5_data.append(item['total'])

 # Gráfico 6 
    fecha_limite = now() - timedelta(days=365)  # fecha hace 12 meses

    servicios_por_mes = Servicio.objects.filter(fecha_inicio_servicio__gte=fecha_limite)\
        .annotate(mes=TruncMonth('fecha_inicio_servicio'))\
        .values('mes')\
        .annotate(total=Count('id_servicio'))\
        .order_by('mes')

    grafico6_labels = []
    grafico6_data = []

    for item in servicios_por_mes:
        mes_str = item['mes'].strftime('%Y-%m')  # formatear fecha a "YYYY-MM"
        grafico6_labels.append(mes_str)
        grafico6_data.append(item['total'])

    # Gráfico 7 
    fallas = Electrodomestico.objects.values('descripcion_falla_electrodomestico')\
        .annotate(frecuencia=Count('id_electrodomestico'))\
        .order_by('-frecuencia')[:10]

    grafico7_labels = [f['descripcion_falla_electrodomestico'] for f in fallas]
    grafico7_data = [f['frecuencia'] for f in fallas]

   # Gráfico 8 
    estados = Factura.objects.values('estado_factura')\
        .annotate(total_facturas=Count('id_factura'))\
        .order_by('-total_facturas')

    grafico8_labels = [e['estado_factura'] for e in estados]
    grafico8_data = [e['total_facturas'] for e in estados]

    pagos = Factura.objects.values('pagado_factura')\
        .annotate(total=Count('id_factura'))\
        .order_by('pagado_factura')

    grafico9_labels = [p['pagado_factura'] for p in pagos]
    grafico9_data = [p['total'] for p in pagos]


    # Gráfico 10 
    clientes_top = Factura.objects.values('id_cliente__nombre_cliente')\
        .annotate(total_facturado=Sum('monto_total_factura'))\
        .order_by('-total_facturado')[:5]

    grafico10_labels = [c['id_cliente__nombre_cliente'] for c in clientes_top]
    grafico10_data = [float(c['total_facturado']) for c in clientes_top]


    return render(request, 'inicio.html', {
        'grafico1_labels': json.dumps(grafico1_labels),
        'grafico1_data': json.dumps(grafico1_data),
        'grafico2_labels': json.dumps(grafico2_labels),
        'grafico2_data': json.dumps(grafico2_data),
        'grafico3_labels': json.dumps(grafico3_labels),
        'grafico3_data': json.dumps(grafico3_data),
        'grafico4_labels': json.dumps(grafico4_labels),
        'grafico4_data': json.dumps(grafico4_data),
        'grafico5_labels': json.dumps(grafico5_labels),
        'grafico5_data': json.dumps(grafico5_data),
        'grafico6_labels': json.dumps(grafico6_labels),
        'grafico6_data': json.dumps(grafico6_data),
        'grafico7_labels': json.dumps(grafico7_labels),
        'grafico7_data': json.dumps(grafico7_data),
        'grafico8_labels': json.dumps(grafico8_labels),
        'grafico8_data': json.dumps(grafico8_data),
        'grafico9_labels': json.dumps(grafico9_labels),
        'grafico9_data': json.dumps(grafico9_data),
        'grafico10_labels': json.dumps(grafico10_labels),
        'grafico10_data': json.dumps(grafico10_data),
    })





#----------------------------- Contactos -----------------------------

def contacto(request):
    return render(request,'contacto.html')

def servicio(request):
    return render(request,'servicio.html')


def nuevologin(request):
    return render(request, 'nuevologin.html')

def listadologin(request):
    logins = Login.objects.all()
    return render(request, 'listadologin.html', {'logins': logins})

def guardarlogin(request):
    nombre = request.POST['txt_nombre']
    contrasena = request.POST['txt_contrasena']
    Login.objects.create(nombre_login=nombre, contrasena_login=contrasena)
    messages.success(request, "Usuario registrado")
    return redirect('/listadologin')

def eliminarlogin(request, id):
    Login.objects.get(id_login=id).delete()
    messages.success(request, "Usuario eliminado")
    return redirect('/listadologin')

def editarlogin(request, id):
    login = Login.objects.get(id_login=id)
    return render(request, 'editarlogin.html', {'login': login})

def procesareditarlogin(request):
    login = Login.objects.get(id_login=request.POST['id'])
    login.nombre_login = request.POST['txt_nombre']
    login.contrasena_login = request.POST['txt_contrasena']
    login.save()
    messages.success(request, "Usuario editado")
    return redirect('/listadologin')




#-------------------------------------------------------- Mostrar formulario para nuevo cliente

def nuevocliente(request):
    logins = Login.objects.all().order_by('nombre_login')
    return render(request, 'nuevocliente.html', {'logins': logins})

# Listar todos los clientes
def listadocliente(request):
    clientes = Cliente.objects.select_related('id_login').all()
    return render(request, 'listadocliente.html', {'clientes': clientes})

# Guardar nuevo cliente
def guardarcliente(request):
    id_login = request.POST['login_id']
    nombre = request.POST['txt_nombre']
    direccion = request.POST['txt_direccion']
    telefono = request.POST['txt_telefono']
    correo = request.POST['txt_correo']

    Cliente.objects.create(
        id_login_id=id_login,
        nombre_cliente=nombre,
        direccion_cliente=direccion,
        telefono_cliente=telefono,
        correo_cliente=correo,
    )
    messages.success(request, "Cliente guardado")
    return redirect('/listadocliente')

# Eliminar cliente
def eliminarcliente(request, id):
    Cliente.objects.get(id_cliente=id).delete()
    messages.success(request, "Cliente eliminado")
    return redirect('/listadocliente')

# Mostrar formulario de edición con datos del cliente
def editarcliente(request, id):
    cliente = Cliente.objects.get(id_cliente=id)
    logins = Login.objects.all()
    return render(request, 'editarcliente.html', {'cliente': cliente, 'logins': logins})

# Procesar edición del cliente
def procesareditarcliente(request):
    cliente = Cliente.objects.get(id_cliente=request.POST['id'])
    cliente.id_login_id = request.POST['login_id']
    cliente.nombre_cliente = request.POST['txt_nombre']
    cliente.direccion_cliente = request.POST['txt_direccion']
    cliente.telefono_cliente = request.POST['txt_telefono']
    cliente.correo_cliente = request.POST['txt_correo']
    cliente.save()
    messages.success(request, "Cliente editado")
    return redirect('/listadocliente')



#-------------------------- Crud de Tecnico --------------------------------

def nuevotecnico(request):
    logins = Login.objects.all().order_by('nombre_login')
    return render(request, 'nuevotecnico.html', {'logins': logins})

def listadotecnico(request):
    tecnicos = Tecnico.objects.select_related('id_login').all()
    return render(request, 'listadotecnico.html', {'tecnicos': tecnicos})

def guardartecnico(request):
    id_login = request.POST['login_id']
    nombre = request.POST['txt_nombre']
    especialidad = request.POST['txt_especialidad']
    telefono = request.POST['txt_telefono']
    correo = request.POST['txt_correo']
    fecha_contratacion = request.POST['txt_fecha_contratacion']

    Tecnico.objects.create(
        id_login_id=id_login,
        nombre_tecnico=nombre,
        especialidad_tecnico=especialidad,
        telefono_tecnico=telefono,
        correo_tecnico=correo,
        fecha_contratacion_tecnico=fecha_contratacion
    )
    messages.success(request, "Técnico guardado")
    return redirect('/listadotecnico')

def eliminartecnico(request, id):
    Tecnico.objects.get(id_tecnico=id).delete()
    messages.success(request, "Técnico eliminado")
    return redirect('/listadotecnico')

def editartecnico(request, id):
    tecnico = Tecnico.objects.get(id_tecnico=id)
    logins = Login.objects.all()
    return render(request, 'editartecnico.html', {'tecnico': tecnico, 'logins': logins})

def procesareditartecnico(request):
    tecnico = Tecnico.objects.get(id_tecnico=request.POST['id'])
    tecnico.id_login_id = request.POST['login_id']
    tecnico.nombre_tecnico = request.POST['txt_nombre']
    tecnico.especialidad_tecnico = request.POST['txt_especialidad']
    tecnico.telefono_tecnico = request.POST['txt_telefono']
    tecnico.correo_tecnico = request.POST['txt_correo']
    tecnico.fecha_contratacion_tecnico = request.POST['txt_fecha_contratacion']
    tecnico.save()
    messages.success(request, "Técnico editado")
    return redirect('/listadotecnico')




#-------------------------------Crud Electrodomestico--------------------------------

def nuevoelectrodomestico(request):
    clientes = Cliente.objects.all().order_by('nombre_cliente')
    return render(request, 'nuevoelectrodomestico.html', {'clientes': clientes})

def listadoelectrodomestico(request):
    electrodomesticos = Electrodomestico.objects.select_related('id_cliente').all()
    return render(request, 'listadoelectrodomestico.html', {'electrodomesticos': electrodomesticos})

def guardarelectrodomestico(request):
    id_cliente = request.POST['cliente_id']
    tipo = request.POST['txt_tipo']
    marca = request.POST['txt_marca']
    modelo = request.POST['txt_modelo']
    descripcion = request.POST['txt_descripcion']
    fecha_ingreso = request.POST['txt_fecha_ingreso']

    Electrodomestico.objects.create(
        id_cliente_id=id_cliente,
        tipo_electrodomestico=tipo,
        marca_electrodomestico=marca,
        modelo_electrodomestico=modelo,
        descripcion_falla_electrodomestico=descripcion,
        fecha_ingreso_electrodomestico=fecha_ingreso
    )
    messages.success(request, "Electrodoméstico guardado")
    return redirect('/listadoelectrodomestico')

def eliminarelectrodomestico(request, id):
    Electrodomestico.objects.get(id_electrodomestico=id).delete()
    messages.success(request, "Electrodoméstico eliminado")
    return redirect('/listadoelectrodomestico')

def editarelectrodomestico(request, id):
    electrodomestico = Electrodomestico.objects.get(id_electrodomestico=id)
    clientes = Cliente.objects.all()
    return render(request, 'editarelectrodomestico.html', {'electrodomestico': electrodomestico, 'clientes': clientes})

def procesareditarelectrodomestico(request):
    electrodomestico = Electrodomestico.objects.get(id_electrodomestico=request.POST['id'])
    electrodomestico.id_cliente_id = request.POST['cliente_id']
    electrodomestico.tipo_electrodomestico = request.POST['txt_tipo']
    electrodomestico.marca_electrodomestico = request.POST['txt_marca']
    electrodomestico.modelo_electrodomestico = request.POST['txt_modelo']
    electrodomestico.descripcion_falla_electrodomestico = request.POST['txt_descripcion']
    electrodomestico.fecha_ingreso_electrodomestico = request.POST['txt_fecha_ingreso']
    electrodomestico.save()
    messages.success(request, "Electrodoméstico editado")
    return redirect('/listadoelectrodomestico')



#------------------------------Crud de Servicio--------------------------------

def nuevoservicio(request):
    tecnicos = Tecnico.objects.all().order_by('nombre_tecnico')
    electrodomesticos = Electrodomestico.objects.all().order_by('tipo_electrodomestico')
    estados = ['Pendiente', 'En Proceso', 'Finalizado']
    return render(request, 'nuevoservicio.html', {
        'tecnicos': tecnicos,
        'electrodomesticos': electrodomesticos,
        'estados': estados
    })

def listadoservicio(request):
    servicios = Servicio.objects.select_related('id_tecnico', 'id_electrodomestico').all()
    return render(request, 'listadoservicio.html', {'servicios': servicios})

def guardarservicio(request):
    id_tecnico = request.POST['tecnico_id']
    id_electrodomestico = request.POST['electrodomestico_id']
    descripcion = request.POST['txt_descripcion']
    costo = request.POST['txt_costo']
    estado = request.POST['select_estado']
    fecha_inicio = request.POST['txt_fecha_inicio']
    fecha_fin = request.POST.get('txt_fecha_fin')  # puede ser vacía

    Servicio.objects.create(
        id_tecnico_id=id_tecnico,
        id_electrodomestico_id=id_electrodomestico,
        descripcion_servicio_servicio=descripcion,
        costo_estimado_servicio=costo,
        estado_servicio=estado,
        fecha_inicio_servicio=fecha_inicio,
        fecha_fin_servicio=fecha_fin if fecha_fin else None,
    )
    messages.success(request, "Servicio guardado")
    return redirect('/listadoservicio')

def eliminarservicio(request, id):
    Servicio.objects.get(id_servicio=id).delete()
    messages.success(request, "Servicio eliminado")
    return redirect('/listadoservicio')

def editarservicio(request, id):
    servicio = Servicio.objects.get(id_servicio=id)
    tecnicos = Tecnico.objects.all()
    electrodomesticos = Electrodomestico.objects.all()
    estados = ['Pendiente', 'En Proceso', 'Finalizado']
    return render(request, 'editarservicio.html', {
        'servicio': servicio,
        'tecnicos': tecnicos,
        'electrodomesticos': electrodomesticos,
        'estados': estados
    })

def procesareditarservicio(request):
    servicio = Servicio.objects.get(id_servicio=request.POST['id'])
    servicio.id_tecnico_id = request.POST['tecnico_id']
    servicio.id_electrodomestico_id = request.POST['electrodomestico_id']
    servicio.descripcion_servicio_servicio = request.POST['txt_descripcion']
    servicio.costo_estimado_servicio = request.POST['txt_costo']
    servicio.estado_servicio = request.POST['select_estado']
    servicio.fecha_inicio_servicio = request.POST['txt_fecha_inicio']
    fecha_fin = request.POST.get('txt_fecha_fin')
    servicio.fecha_fin_servicio = fecha_fin if fecha_fin else None
    servicio.save()
    messages.success(request, "Servicio editado")
    return redirect('/listadoservicio')





#------------------------------ Crud de Factura --------------------------------

def nuevafactura(request):
    clientes = Cliente.objects.all().order_by('nombre_cliente')
    servicios = Servicio.objects.all()
    opciones_pagado = ['Si', 'No']
    opciones_estado = ['Vigente', 'Expirada']
    return render(request, 'nuevafactura.html', {
        'clientes': clientes,
        'servicios': servicios,
        'opciones_pagado': opciones_pagado,
        'opciones_estado': opciones_estado,
    })

def listadofactura(request):
    facturas = Factura.objects.select_related('id_cliente', 'id_servicio').all()
    return render(request, 'listadofactura.html', {'facturas': facturas})

def guardarfactura(request):
    id_cliente = request.POST['cliente_id']
    id_servicio = request.POST['servicio_id']
    monto = request.POST['txt_monto']
    pagado = request.POST['select_pagado']
    estado = request.POST['select_estado']
    tiempo = request.POST['txt_tiempo']

    Factura.objects.create(
        id_cliente_id=id_cliente,
        id_servicio_id=id_servicio,
        monto_total_factura=monto,
        pagado_factura=pagado,
        estado_factura=estado,
        tiempo_factura=tiempo
    )
    messages.success(request, "Factura guardada")
    return redirect('/listadofactura')

def eliminarfactura(request, id):
    Factura.objects.get(id_factura=id).delete()
    messages.success(request, "Factura eliminada")
    return redirect('/listadofactura')

def editarfactura(request, id):
    factura = Factura.objects.get(id_factura=id)
    clientes = Cliente.objects.all()
    servicios = Servicio.objects.all()
    opciones_pagado = ['Si', 'No']
    opciones_estado = ['Vigente', 'Expirada']
    return render(request, 'editarfactura.html', {
        'factura': factura,
        'clientes': clientes,
        'servicios': servicios,
        'opciones_pagado': opciones_pagado,
        'opciones_estado': opciones_estado,
    })

def procesareditarfactura(request):
    factura = Factura.objects.get(id_factura=request.POST['id'])
    factura.id_cliente_id = request.POST['cliente_id']
    factura.id_servicio_id = request.POST['servicio_id']
    factura.monto_total_factura = request.POST['txt_monto']
    factura.pagado_factura = request.POST['select_pagado']
    factura.estado_factura = request.POST['select_estado']
    factura.tiempo_factura = request.POST['txt_tiempo']
    factura.save()
    messages.success(request, "Factura editada")
    return redirect('/listadofactura')
