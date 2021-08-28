from django.db import models
from django.contrib.auth.models import User

class perfil(models.Model):
    perfilID=models.AutoField(primary_key=True)
    nombrePerfil=models.CharField(max_length = 50)
    def __str__(self):
        return '%s'%(self.nombrePerfil)

class tematicas(models.Model):
    temaNombre=models.CharField(max_length=50, null=True)
    perfilId=models.ForeignKey(perfil,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return '%s'%(self.temaNombre)

class libros(models.Model):

    titulo=models.CharField(max_length = 50)
    perfilId=models.ForeignKey(perfil,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.titulo

class solucionadores(models.Model):
    solucionadorNombre=models.CharField(max_length = 50)
    solucionadorPais=models.CharField(max_length = 50)
    solucionadorID=models.AutoField(primary_key=True)
    solucionadorPais=models.CharField(max_length = 50)
    def __str__(self):
        return self.solucionadorNombre

class paquetes(models.Model):
    paqueteID=models.AutoField(primary_key=True)
    paqueteCod=models.CharField(max_length=50, null=True)
    paqueteCant=models.IntegerField(null=True)
    paquetePrecio=models.IntegerField(null=True)
    paqueteDias=models.IntegerField(null=True)
    paqueteDescr=models.CharField(max_length=50, null=True)
    paquetePerfil=models.ForeignKey(perfil, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return '%s'%(self.paqueteCod)

class soluciones(models.Model):
    problemaNumero=models.CharField(max_length=50, null=True)
    problemaProblema=models.ImageField(upload_to='problemas', null=True)
    problemaID=models.AutoField(primary_key=True)
    problemaLibro=models.ForeignKey(libros, on_delete=models.CASCADE,null=True)
    problemaSolucion=models.FileField(upload_to='soluciones',null=True)
    problemaVideo=models.FileField(upload_to='videos',null=True)
    problemaSolucionadoPor=models.ForeignKey(solucionadores, on_delete=models.CASCADE,null=True)
    problemaTema=models.ForeignKey(tematicas, on_delete=models.CASCADE,null=True)
    def __str__(self):
        return '%s%s'%(self.problemaNumero,self.problemaProblema)

class UsuarioPaq(models.Model):
    usuario=models.IntegerField(null=True)
    fechaIni=models.DateField(blank=True, null=True)
    fechaPago=models.DateField(blank=True, null=True)
    paqueteMio=models.ForeignKey(paquetes,on_delete=models.CASCADE,null=True)
    activo=models.BooleanField(blank=True, null=True)
    vencido=models.BooleanField(blank=True, null=True,default=False)
    def __str__(self):
        return '%s%s'%(self.usuario,self.paqueteMio)

class ProblemaPaq(models.Model):
    problemaID= models.ForeignKey(soluciones,on_delete=models.CASCADE,null=True)
    paqueteID= models.ForeignKey(paquetes,on_delete=models.CASCADE,null=True)

class QRPago(models.Model):
    qr=models.ImageField(upload_to='qr', null=True)
    Nombre=models.CharField(max_length=50, null=True)
    foto=models.ImageField(upload_to='foto', null=True,blank=True)
    

	
