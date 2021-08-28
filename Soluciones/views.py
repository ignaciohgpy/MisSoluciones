from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from Soluciones.models import libros, soluciones, paquetes,tematicas,UsuarioPaq,QRPago,perfil,ProblemaPaq
from Soluciones.forms import Formulario
from django.db.models import Count,Sum
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
import datetime as fecha
import json,threading,time

def acerca(request):
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    perfiles=perfil.objects.all()
    return render(request,"acercaDe.html" ,{'perfiles':perfiles,"mispaquetes":paquetesUsu})

def vencimiento():
    QActivos= UsuarioPaq.objects.select_related().filter(activo=True)
    while True:
        for h in QActivos:
            fechaVence=h.fechaPago+fecha.timedelta(days=h.paqueteMio.paqueteDias)
            if fechaVence<fecha.date.today():
                UsuarioPaq.objects.filter(id=h.id).update(vencido=True,activo=False)
        time.sleep(60)

#hilo=threading.Thread(target=vencimiento())
#hilo.start()

class Addlibros(ListView):
    model=libros
    template_name = "ListaLibros.html"
class Login(LoginView):
    template_name = 'login.html'
class Logout(LogoutView):
    template_name = 'index.html'

def ejemplo(request):
    vpaq= paquetes.objects.all()
    solucion=soluciones.objects.all()[:10]
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)

    perfiles=perfil.objects.all()
    return render(request,"ejemplo.html" ,{'mispaquetes':paquetesUsu,'perfiles':perfiles,'solucion':solucion,'vpaq':vpaq})

def mipkt(request,pkt):
	
    try:
        problemas=ProblemaPaq.objects.select_related("paqueteID","problemaID").filter(paqueteID__paqueteCod=pkt)
        paquetesUsuES=UsuarioPaq.objects.filter(usuario=request.user.id,paqueteMio=paquetes.objects.get(paqueteCod=pkt)).values()[0]
        paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id)
        perfiles=perfil.objects.all()
        qr=QRPago.objects.all()
        return render(request,"verMiPKT.html" ,{'perfiles':perfiles,'pkt':pkt,'qr':qr,'mispaquetes':paquetesUsu,'activo':paquetesUsuES['activo'],'problemas':problemas})
    except:
        redirect('index')

# for u in  paquetesUsuES:
			 # print(u.activo)
		# vpaq= paquetes.objects.all()
		# paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id)
		# paquetesUsuES=UsuarioPaq.objects.filter(usuario=request.user.id,paqueteMio=paquetes.objects.get(paqueteCod=pkt)).values()[0]['id']
		# activo=UsuarioPaq.objects.get(usuario=request.user.id,paqueteMio=paquetes.objects.get(paqueteCod=pkt))
		

def TranferMovil(request,pkt,usuario):
    usuario=request.GET.get("usuario")
    paquete=request.GET.get("paquete")
    codigo='{0}Z{1}'.format(paquete,usuario)
    negocio="TTAAMM"
    lista1=[codigo,negocio]
    contact1 = dict(
        first_name='John',
        last_name='Doe',
        first_name_reading='jAAn',
        last_name_reading='dOH',
        tel='+41769998877',
        email='j.doe@company.com',
        url='http://www.company.com',

    )
    data={'verificado':'ok','sms':"Tranccion Realizada",'qr':contact1 }
    return render(request,'transfermovil.html',data)

def registrarse(request):
    if request.user.is_authenticated:
        return redirect('index', username=request.user.username)
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('index')

    else:
        f = CustomUserCreationForm()

    return render(request, 'registrarse.html', {'form': f})
def consultar(request):
    solucionesTabla=soluciones.objects.all()
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    perfiles=perfil.objects.all()
    vpaq= paquetes.objects.all()
    return render(request,'busquedas.html',{'data':solucionesTabla, 'perfiles':perfiles, 'vpaq':vpaq, 'mispaquetes':paquetesUsu})
def problema(request,libro):
    id=libros.objects.get(titulo=libro)
    problemas=soluciones.objects.filter(problemaLibro=id)
    problemas10=soluciones.objects.filter(problemaLibro=id)[:2]
    arbol={}
    for y in problemas:

        arbol[y.problemaTema.temaNombre]=[]
    for v in problemas:
        arbol[v.problemaTema.temaNombre].append(v.problemaNumero)
    data={'libro':libro, 'problemas':problemas,'arbol':arbol,'tamara':problemas10}
    return render(request,"problema.html", data)


def versolucion(request,libro, numero):
    id=libros.objects.get(titulo=libro)
    solucion=soluciones.objects.get(problemaLibro=id, problemaNumero=numero)

    return render(request,"versolucion.html", {'solucion':solucion})

def verPKT(request):

    libro=request.GET.get('libro',None)
    numero=request.GET.get('problema',None)
    solucion=soluciones.objects.get(problemaLibro=libros.objects.get(titulo=libro),problemaNumero=numero)
    activo=UsuarioPaq.objects.get(usuario=request.user.id)

    return render(request,"versolucion.html", {'solucion':solucion})

def compraPKT(request):
    
    codigoPKT=request.GET.get('tema', None).split(',')[0]
   
    usuarioID=int(request.user.id)
    fecha1=fecha.date.today()
    puede=UsuarioPaq.objects.filter(usuario=usuarioID,paqueteMio=paquetes.objects.get(paqueteCod=codigoPKT))
    if len(puede)!=0:
        tema="Ya usted tiene ese paquete"
        tipo=1
    else:
        try:
            UsuarioPaq.objects.create(usuario=usuarioID, fechaIni= fecha1, paqueteMio=paquetes.objects.get(paqueteCod=codigoPKT),activo="False")
            tema="Ha adquirido un paquete"
            tipo=2

        except:
            tema="Ha ocurrido un error"
            tipo=1
    data = {'sms': tema,'tipo':tipo}
    return JsonResponse(data)

def borraPa(request):
    valor=request.GET.get("paquete")

    try:
        UsuarioPaq.objects.select_related('paqueteMio').filter(paqueteMio__paqueteCod=valor).delete()
        tema="El registro ha sido eliminado."
        tipo=2
        data = {'sms': tema,'tipo':tipo}
    except:
        tema="Ha ocurrido un error"
        tipo=1
        data = {'sms': tema,'tipo':tipo}

    return JsonResponse(data)

def getProblemas(request):
    problemas = request.GET.get('problemas', None)
    ProblS=soluciones.objects.filter(problemaPkt=paquetes.objects.get(paqueteCod=problemas))

    lista=[]
    for u in ProblS:
        lista.append(u.problemaNumero)

    problemasLista=[]
    while len(lista) >3:
         pice = lista[:3]
         problemasLista.append(pice)
         lista   = lista[3:]
         problemasLista.append(lista)

    a=json.dumps(problemasLista)

    data = {'problemas': a}

    return JsonResponse(data)

def index(request):
    orden={}
    admin=""
    pket=""
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)

    perfiles=perfil.objects.all()
    vpaq= paquetes.objects.all()
    temas=tematicas.objects.all()
    if  not request.user.is_staff:
        admin="pointer-events:none;cursor:default"
    if  not request.user.is_authenticated:
        pket="pointer-events:none;cursor:default"
    u=soluciones.objects.values('problemaLibro').annotate(num_books=Count('problemaLibro'))
    total=soluciones.objects.count()
    for i in range(0,len(u)):
        libro=libros.objects.get(id=int(u[i]['problemaLibro']))
        orden[libro.titulo]=u[i]['num_books']

    return render(request,"index.html", {'perfiles':perfiles,'mispaquetes':paquetesUsu,'libros':orden,'total':total,'admin':admin,"pket":pket, "vpaq": vpaq,"temas":temas})


def getPaquetes(request):
    perfil=request.GET.get('perfil', None)

    paquetes1=paquetes.objects.select_related('paquetePerfil').filter(paquetePerfil__nombrePerfil=perfil)
    lista=[]
    for h in paquetes1:
        lista.append('{0}, {2} de {1}'.format(h.paqueteCod,h.paqueteDescr,h.paqueteCant))
    data= {'paquetes':list(lista)}
    return JsonResponse(data)

def getDetalles(request):
    cadena=request.GET.get('CodigoP', None).split(',')
    
    paquetes1=paquetes.objects.values().get(paqueteCod=cadena[0])
    
    lista=[]
    for h in paquetes1.keys():
       lista.append(paquetes1[h])
       
    data= {'paquetes':list(lista)}
    return JsonResponse(data)
def cargar(request):

   libros1=libros.objects.all()

   data={'formulario':Formulario(),'libros':libros1}
   if request.method=="POST":
       formulario=Formulario(data=request.POST, files=request.FILES)
       if formulario.is_valid():
           formulario.save()
           data["mensaje"]="Todo OK"
       else:
           data["formulario"]=formulario
   return render(request, "cargar.html" ,data)

def ver(request):
    solu=soluciones.objects.all()
    return render(request, "ver.html" ,{"soluciones":solu})
