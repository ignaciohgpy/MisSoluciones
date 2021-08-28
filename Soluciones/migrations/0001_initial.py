# Generated by Django 3.0.6 on 2021-08-28 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='libros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='paquetes',
            fields=[
                ('paqueteID', models.AutoField(primary_key=True, serialize=False)),
                ('paqueteCod', models.CharField(max_length=50, null=True)),
                ('paqueteCant', models.IntegerField(null=True)),
                ('paquetePrecio', models.IntegerField(null=True)),
                ('paqueteDias', models.IntegerField(null=True)),
                ('paqueteDescr', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='perfil',
            fields=[
                ('perfilID', models.AutoField(primary_key=True, serialize=False)),
                ('nombrePerfil', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QRPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr', models.ImageField(null=True, upload_to='qr')),
                ('Nombre', models.CharField(max_length=50, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='foto')),
            ],
        ),
        migrations.CreateModel(
            name='solucionadores',
            fields=[
                ('solucionadorNombre', models.CharField(max_length=50)),
                ('solucionadorID', models.AutoField(primary_key=True, serialize=False)),
                ('solucionadorPais', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioPaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.IntegerField(null=True)),
                ('fechaIni', models.DateField(blank=True, null=True)),
                ('fechaPago', models.DateField(blank=True, null=True)),
                ('activo', models.BooleanField(blank=True, null=True)),
                ('vencido', models.BooleanField(blank=True, default=False, null=True)),
                ('paqueteMio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.paquetes')),
            ],
        ),
        migrations.CreateModel(
            name='tematicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temaNombre', models.CharField(max_length=50, null=True)),
                ('perfilId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.perfil')),
            ],
        ),
        migrations.CreateModel(
            name='soluciones',
            fields=[
                ('problemaNumero', models.CharField(max_length=50, null=True)),
                ('problemaProblema', models.ImageField(null=True, upload_to='problemas')),
                ('problemaID', models.AutoField(primary_key=True, serialize=False)),
                ('problemaSolucion', models.FileField(null=True, upload_to='soluciones')),
                ('problemaVideo', models.FileField(null=True, upload_to='videos')),
                ('problemaLibro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.libros')),
                ('problemaSolucionadoPor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.solucionadores')),
                ('problemaTema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.tematicas')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemaPaq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paqueteID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.paquetes')),
                ('problemaID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.soluciones')),
            ],
        ),
        migrations.AddField(
            model_name='paquetes',
            name='paquetePerfil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.perfil'),
        ),
        migrations.AddField(
            model_name='libros',
            name='perfilId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Soluciones.perfil'),
        ),
    ]
