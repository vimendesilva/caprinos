# Generated by Django 2.0 on 2018-05-16 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('animais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rgb_animal', models.CharField(blank=True, max_length=50, verbose_name='RGD')),
                ('nome_animal', models.CharField(blank=True, max_length=50, verbose_name='Nome')),
                ('numero_animal', models.IntegerField(verbose_name='Numero')),
                ('sexo_animal', models.BooleanField(verbose_name='Sexo')),
                ('nascimento_animal', models.DateField(blank=True, default=None, null=True, verbose_name='Nascimento')),
                ('raca_animal', models.CharField(max_length=50, verbose_name='Raça')),
                ('sangue_animal', models.CharField(blank=True, max_length=50, verbose_name='Sangue')),
                ('brincos_animal', models.CharField(max_length=50, verbose_name='Brincos')),
                ('chifres_animal', models.BooleanField(verbose_name='Chifres')),
                ('vida_animal', models.BooleanField(verbose_name='Vida')),
                ('observacao_animal', models.TextField(blank=True, verbose_name='Observação')),
                ('id_fazenda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Fazenda', verbose_name='Fazenda')),
            ],
            options={
                'verbose_name': 'Animal',
            },
        ),
        migrations.RemoveField(
            model_name='bode',
            name='id_fazenda',
        ),
        migrations.RemoveField(
            model_name='cabra',
            name='id_fazenda',
        ),
        migrations.RemoveField(
            model_name='filhote',
            name='id_parto',
        ),
        migrations.RemoveField(
            model_name='cobertura',
            name='data_cobertura',
        ),
        migrations.AddField(
            model_name='cobertura',
            name='fim_cobertura',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Fim'),
        ),
        migrations.AddField(
            model_name='cobertura',
            name='inicio_cobertura',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Início'),
        ),
        migrations.AlterField(
            model_name='cobertura',
            name='id_bode',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Bode', to='animais.Animal', verbose_name='Bode'),
        ),
        migrations.AlterField(
            model_name='cobertura',
            name='id_cabra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cabra', to='animais.Animal', verbose_name='Cabra'),
        ),
        migrations.AlterField(
            model_name='producao',
            name='id_cabra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Animal', verbose_name='Cabra'),
        ),
        migrations.DeleteModel(
            name='Bode',
        ),
        migrations.DeleteModel(
            name='Cabra',
        ),
        migrations.DeleteModel(
            name='Filhote',
        ),
    ]