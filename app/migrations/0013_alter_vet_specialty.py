# Generated by Django 5.0.4 on 2024-05-19 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_vet_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vet',
            name='specialty',
            field=models.CharField(choices=[('Medicina interna', 'Medicina interna'), ('Cirugía', 'Cirugía'), ('Dermatología', 'Dermatología'), ('Oftalmología', 'Oftalmología'), ('Odontología', 'Odontología'), ('Oncología', 'Oncología'), ('Ortopedia', 'Ortopedia'), ('Cardiología', 'Cardiología'), ('Neurología', 'Neurología'), ('Reproducción', 'Reproducción')], default='Medicina interna', max_length=50),
        ),
    ]
