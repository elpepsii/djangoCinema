from django.db import models

# Create your models here.

class Peliculas(models.Model):
    nombre=models.CharField(max_length=50)
    director=models.CharField(max_length=50)
    anno=models.PositiveBigIntegerField()
    duracion=models.PositiveIntegerField()
    imagen=models.ImageField(upload_to="peliculas")

    def __str__(self):
        return self.nombre + " (" + str(self.anno) + ")"

class Funcion(models.Model):
    pelicula=models.ForeignKey(Peliculas, on_delete=models.CASCADE)
    fecha=models.DateField()
    hora=models.TimeField()
    precio=models.PositiveIntegerField()
    asientos_disponibles=models.PositiveIntegerField()
    asientos_vendidos=models.PositiveIntegerField()
    sala=models.CharField(max_length=50)

    def __str__(self):
        return self.pelicula.nombre
    
class Ventas(models.Model):
    funcion=models.ForeignKey(Funcion, on_delete=models.CASCADE)
    cliente=models.CharField(max_length=50)
    email=models.CharField(max_length=50, blank=True)
    codigo=models.CharField(max_length=50, blank=True)
    entradas=models.PositiveIntegerField()
    total_original=models.PositiveIntegerField(default=0)
    total_descuento=models.PositiveIntegerField(default=0)
    total_final=models.PositiveIntegerField(default=0)
    fecha=models.DateField()