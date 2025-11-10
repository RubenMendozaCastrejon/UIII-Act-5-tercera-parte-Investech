from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Usuario, Portafolio, Activo
from datetime import datetime

def inicio_usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/ver_usuario.html', {'usuarios': usuarios})

def agregar_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        pais = request.POST.get('pais')
        saldo_disponible = request.POST.get('saldo_disponible', 0.00)
        
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            pais=pais,
            saldo_disponible=saldo_disponible
        )
        usuario.save()
        return redirect('inicio_usuario')
    
    return render(request, 'usuario/agregar_usuario.html')

def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})

def realizar_actualizacion_usuario(request, usuario_id):
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=usuario_id)
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.email = request.POST.get('email')
        usuario.telefono = request.POST.get('telefono')
        usuario.pais = request.POST.get('pais')
        usuario.saldo_disponible = request.POST.get('saldo_disponible', 0.00)
        usuario.save()
        return redirect('inicio_usuario')  # Redirige a la lista después de actualizar
    
    # Si no es POST, muestra el formulario de actualización
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})

def borrar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('inicio_usuario')
    
    return render(request, 'usuario/borrar_usuario.html', {'usuario': usuario})

def inicio(request):
    return render(request, 'inicio.html')

# ... después de las funciones de Usuario ...

def inicio_portafolio(request):
    portafolios = Portafolio.objects.all()
    return render(request, 'portafolio/ver_portafolio.html', {'portafolios': portafolios})

def agregar_portafolio(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        valor_total = request.POST.get('valor_total', 0.00)
        riesgo = request.POST.get('riesgo')
        activos_ids = request.POST.getlist('activos')  # ← Obtener múltiples activos
        
        usuario = Usuario.objects.get(id=usuario_id)
        portafolio = Portafolio(
            usuario=usuario,
            nombre=nombre,
            descripcion=descripcion,
            valor_total=valor_total,
            riesgo=riesgo
        )
        portafolio.save()
        
        # Agregar los activos seleccionados al portafolio
        if activos_ids:
            activos = Activo.objects.filter(id__in=activos_ids)
            portafolio.activos.set(activos)
        
        return redirect('inicio_portafolio')
    
    usuarios = Usuario.objects.all()
    activos = Activo.objects.all()  # ← Obtener todos los activos para el combobox
    return render(request, 'portafolio/agregar_portafolio.html', {
        'usuarios': usuarios,
        'activos': activos
    })

def actualizar_portafolio(request, portafolio_id):
    portafolio = get_object_or_404(Portafolio, id=portafolio_id)
    usuarios = Usuario.objects.all()
    activos = Activo.objects.all()  # ← Obtener todos los activos
    return render(request, 'portafolio/actualizar_portafolio.html', {
        'portafolio': portafolio,
        'usuarios': usuarios,
        'activos': activos
    })

def realizar_actualizacion_portafolio(request, portafolio_id):
    if request.method == 'POST':
        portafolio = get_object_or_404(Portafolio, id=portafolio_id)
        usuario_id = request.POST.get('usuario')
        activos_ids = request.POST.getlist('activos')  # ← Obtener múltiples activos
        
        portafolio.usuario = Usuario.objects.get(id=usuario_id)
        portafolio.nombre = request.POST.get('nombre')
        portafolio.descripcion = request.POST.get('descripcion')
        portafolio.valor_total = request.POST.get('valor_total', 0.00)
        portafolio.riesgo = request.POST.get('riesgo')
        portafolio.save()
        
        # Actualizar los activos del portafolio
        if activos_ids:
            activos = Activo.objects.filter(id__in=activos_ids)
            portafolio.activos.set(activos)
        else:
            portafolio.activos.clear()
        
        return redirect('inicio_portafolio')
    
    return redirect('inicio_portafolio')

def borrar_portafolio(request, portafolio_id):
    portafolio = get_object_or_404(Portafolio, id=portafolio_id)
    if request.method == 'POST':
        portafolio.delete()
        return redirect('inicio_portafolio')
    
    return render(request, 'portafolio/borrar_portafolio.html', {'portafolio': portafolio})

# ... después de las funciones de Portafolio ...

# --- VISTAS PARA ACTIVO ---
def inicio_activo(request):
    activos = Activo.objects.all()
    return render(request, 'activo/ver_activo.html', {'activos': activos})

def agregar_activo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        simbolo = request.POST.get('simbolo')
        precio_actual = request.POST.get('precio_actual', 0.00)
        mercado = request.POST.get('mercado')
        volatilidad = request.POST.get('volatilidad', 0.00)
        
        activo = Activo(
            nombre=nombre,
            tipo=tipo,
            simbolo=simbolo,
            precio_actual=precio_actual,
            mercado=mercado,
            volatilidad=volatilidad
        )
        activo.save()
        return redirect('inicio_activo')
    
    return render(request, 'activo/agregar_activo.html')

def actualizar_activo(request, activo_id):
    activo = get_object_or_404(Activo, id=activo_id)
    return render(request, 'activo/actualizar_activo.html', {'activo': activo})

def realizar_actualizacion_activo(request, activo_id):
    if request.method == 'POST':
        activo = get_object_or_404(Activo, id=activo_id)
        activo.nombre = request.POST.get('nombre')
        activo.tipo = request.POST.get('tipo')
        activo.simbolo = request.POST.get('simbolo')
        activo.precio_actual = request.POST.get('precio_actual', 0.00)
        activo.mercado = request.POST.get('mercado')
        activo.volatilidad = request.POST.get('volatilidad', 0.00)
        activo.save()
        return redirect('inicio_activo')
    
    return redirect('inicio_activo')

def borrar_activo(request, activo_id):
    activo = get_object_or_404(Activo, id=activo_id)
    if request.method == 'POST':
        activo.delete()
        return redirect('inicio_activo')
    
    return render(request, 'activo/borrar_activo.html', {'activo': activo})