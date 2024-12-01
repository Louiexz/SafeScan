# Generated by Django 5.1.2 on 2024-11-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safescan', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='software',
            old_name='status',
            new_name='label',
        ),
        migrations.AddField(
            model_name='software',
            name='arquivos_confOS',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='biblioteca_class',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='bluetooth_funcionalidades',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='camera',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='localizacao_rede',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='midia_audio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='pacotes',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='rede_operadora',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='sim_pais',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='software',
            name='sms',
            field=models.BooleanField(default=False),
        ),
    ]