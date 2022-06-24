from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from Soluciones.models import libros, soluciones, paquetes,tematicas,UsuarioPaq,QRPago,perfil,ProblemaPaq,User, comentarios
from Soluciones.forms import Formulario
from django.db.models import Count,Sum
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.contrib.auth.views import  LogoutView
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect


import datetime as fecha
from django.contrib.auth.decorators import login_required
import json,threading,time

def contactanos(request):
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    perfiles=perfil.objects.all()
    return render(request,"contactanos.html" ,{'perfiles':perfiles,"mispaquetes":paquetesUsu, "novalida":"none"})

class ListaLibros(ListView):
    template_name = "libros_list.html"
    model = libros


    def get_context_data(self,**kwargs):
        context=super(ListaLibros,self).get_context_data(**kwargs)
        context.update({'novalida':'none'})
        return context

class CreaLibro(CreateView):
    model = libros
    template_name = "libros_form.html"
    success_url = reverse_lazy('listalibros')
    fields = ['titulo', 'perfilId']
    def get_context_data(self,**kwargs):
        context=super(CreaLibro,self).get_context_data(**kwargs)
        context.update({'novalida':'none'})
        return context

class BorraLibro(DeleteView):
    model = libros
    success_url = reverse_lazy('listalibros')
    def get_context_data(self,**kwargs):
        context=super(BorraLibro,self).get_context_data(**kwargs)
        context.update({'novalida':'none'})
        return context

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

def registro1(request):
    m = 3;
    return render(request, 'registro.html')

def team(request):
    data=completarPlantilla(request)
    return render(request, 'team.html',data)
def promociones(request):
    m = 3;
    return render(request, 'promociones.html')


def LPaquetes(request,miperfil): #OK
    perfiles=perfil.objects.values()
    
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, vencido=False)
    paquete=paquetes.objects.select_related('paquetePerfil').filter(paquetePerfil__nombrePerfil=miperfil)
    datos={'perfil':miperfil,'novalida':"none","paquetes":paquete,'perfiles':perfiles,'mispaquetes':paquetesUsu,'estilo':"display:none"}

    return render(request, 'listarPaquetes.html',datos )

def Milogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            username = username.strip()            # Eliminar espacios y líneas nuevas
            password = password.strip()
            try:
                user = User.objects.get(username=username)
            except:
                message = 'El nombre de usuario no existe'
                return render(request, 'login.html', {"message": message})
            if user.check_password(password):
                request.session['id'] = user.id    # Registrar que el usuario ha iniciado sesión
                user = authenticate(username=username, password=password)

                request.session['id'] = user.id
                login(request, user)
                perfiles=perfil.objects.all()
                return render(request,'index.html',{'novalida':'none','perfiles':perfiles})
            else:
                message = 'contraseña incorrecta'
                return render(request, 'login.html', {'novalida':'si',"message": message})
    return render(request, 'login.html', {'novalida':'none','estilo':"display:none"})

def logout(request): #OK
    request.session.flush()
    return redirect('/')

def registro(request): #OK
   #if request.session.get('id') != None:  # Regístrese solo cuando no haya iniciado sesión
        #return redirect('/')
   if request.method == 'POST':
        username = request.POST.get('username')
        clave = request.POST.get('password')
        correo=request.POST.get('correo')
        username = str(username).strip()  # Eliminar espacios y líneas nuevas
        clave = str(clave).strip()
        correo=str(correo).strip()
        if User.objects.filter(username=username).exists():
            message = 'este nombre de usuario ha sido registrado'
            return render(request, 'index.html', {"message": message})
        user = User()
        user.username = username

        user.password=make_password(clave)
        user.email=correo
        user.save()
        #request.session['id'] = user.id   # Registrar que el usuario ha iniciado sesión
        return redirect('/')
   return render(request, 'index.html')
def verPaquetes(request,codigo): #ok
    paquetes = ProblemaPaq.objects.select_related('problemaID', 'paqueteID').filter(paqueteID__paqueteCod=codigo)
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, vencido=False)
    perfiles=perfil.objects.all()
    return render(request,"verPaquetes.html" ,{'perfiles':perfiles,'novalida':'none','paquetes':paquetes,'mispaquetes': paquetesUsu ,'estilo':"display:none"})
@login_required(login_url='/login/') #OK
def mipkt(request,pkt):
    print(pkt)
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, paqueteMio=paquetes.objects.get(paqueteCod=pkt))
    if len(paquetesUsu) !=0 :
        problemas=ProblemaPaq.objects.select_related("paqueteID","problemaID").filter(paqueteID__paqueteCod=pkt)
        mispaquetes= UsuarioPaq.objects.filter(usuario=request.user.id)
        return render(request, "verMiPKT.html", {'novalida':'none','pkt': pkt, 'mispaquetes': mispaquetes, 'problemas': problemas,'estilo':"display:none"})
    else:
        redirect('index')





		

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

@login_required(login_url='/login/')
def versolucion(request,libro, numero):
    print(libro)
    print(numero)
    id=libros.objects.get(titulo=libro)
    solucion=soluciones.objects.get(problemaLibro=id, problemaNumero=numero)
    mispaquetes=UsuarioPaq.objects.select_related('paqueteMio').filter(usuario=request.user.id)
    return render(request,"versolucion.html", {'solucion':solucion})



def compraPKT(request): #OK
    
    codigo=request.GET.get('codigo', None)
    usuarioID=int(request.user.id)
    fecha1=fecha.date.today()
    puede=UsuarioPaq.objects.filter(usuario=usuarioID,paqueteMio=paquetes.objects.get(paqueteCod=codigo))
    if len(puede)!=0:
        tema="Ya usted tiene ese paquete"
        tipo=1
    else:
        try:
            UsuarioPaq.objects.create(usuario=usuarioID, fechaIni= fecha1, paqueteMio=paquetes.objects.get(paqueteCod=codigo),activo="False")
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

    pket=""
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)

    perfiles=perfil.objects.values()
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

    return render(request,"index.html", {'novalida':'none','perfiles':perfiles,'mispaquetes':paquetesUsu,'libros':orden,'total':total,'estilo':"display:none","pket":pket, "vpaq": vpaq,"temas":temas})

def completarPlantilla(request):
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    perfiles=perfil.objects.values()
    vpaq= paquetes.objects.all()
    temas=tematicas.objects.all()
    librosT=libros.objects.all()
    configura={'novalida':'none','perfiles':perfiles,'mispaquetes':paquetesUsu,'libros':librosT, "temas":temas}
    return configura
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
def contac(request):
    nombre=request.POST.get("nombre")
    correo=request.POST.get("email")
    tipo=request.POST.get("subject")
    comentario=request.POST.get("message")
    usuario=User.objects.get(id=request.user.id)
    comentarios.objects.create(nombre=nombre,usuario=usuario,correo=correo,tipo=tipo,comentario=comentario)
    data=completarPlantilla(request)
    return render(request,"contactanos.html",data)

def formaPket(request):
    data=completarPlantilla(request)
    return render(request,"FormaPKT.html",data)
def BuscaProblemas(request):
    libro=request.GET.get('libro', None)
    temas=request.GET.get('temas', None)
    problemas1=soluciones.objects.select_related("problemaLibro","problemaTema").filter(problemaLibro__titulo=libro,problemaTema__temaNombre=temas)
    lista=[]
    for u in problemas1:
        if u.problemaNumero not in lista:
            lista.append(u.problemaNumero)
    
    data= {'problemas':list(lista)}

    return JsonResponse(data)
def BuscaTemasxLibros(request):
    libro=request.GET.get('libro', None)
    temas=soluciones.objects.select_related("problemaLibro","problemaTema").filter(problemaLibro__titulo=libro)
    lista=[]
    for u in temas:
        if u.problemaTema.temaNombre not in lista:
            lista.append(u.problemaTema.temaNombre)


    data= {'temas':list(lista)}
    return JsonResponse(data)
def Muestraproblemas(request):
    pro=request.GET.getlist('problemas[]',None)
    problemas=soluciones.objects.filter(problemaNumero__in=pro)
    lista=[]
    for h in problemas:
        lista.append(h.problemaProblema.url)

    data= {'temas':list(lista)}
    return JsonResponse(data)
def cargar(request): #agrega libros

   libros1=libros.objects.all()
   perfiles=perfil.objects.all()
   data={'formulario':Formulario(),'libros':libros1,"novalida":"none","perfiles":perfiles}
   if request.method=="POST":
       formulario=Formulario(data=request.POST, files=request.FILES)
       if formulario.is_valid():
           formulario.save()
           data["mensaje"]="Todo OK"
       else:
           data["formulario"]=formulario
   return render(request, "cargar.html" ,data)

def Creacodigo(request):
    Cod1=request.user.username
    Cod2=request.user.first_name
    Cod3=request.user.last_name

    fecha1=fecha.datetime.now()

    codigo=str(Cod1[0].upper())+str(Cod2[0].upper())+str(Cod3[0].upper())+str(fecha1.year)+str(fecha1.month)+str(fecha1.day)+str(fecha1.hour)+str(fecha1.minute)
    data= {'codigo':codigo}
    return JsonResponse(data)

