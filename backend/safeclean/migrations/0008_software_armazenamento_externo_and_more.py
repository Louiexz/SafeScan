# Generated by Django 5.1.2 on 2024-11-02 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safeclean', '0007_alter_software_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='armazenamento_externo',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software',
            name='audio_hardware',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software',
            name='localizacao_rede',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software',
            name='mensagens_chamada',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='software',
            name='sistema_processos',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
