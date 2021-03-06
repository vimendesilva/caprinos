# Generated by Django 2.0 on 2018-04-22 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_bode', models.CharField(blank=True, max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Bode',
            },
        ),
        migrations.CreateModel(
            name='Cabra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rgd_cabra', models.CharField(blank=True, max_length=50, verbose_name='RGD')),
                ('nome_cabra', models.CharField(blank=True, max_length=50, verbose_name='Nome')),
                ('numero_cabra', models.IntegerField(verbose_name='Numero')),
                ('nascimento_cabra', models.DateField(blank=True, default=None, null=True, verbose_name='Nascimento')),
                ('raca_cabra', models.CharField(max_length=50, verbose_name='Raça')),
                ('sangue_cabra', models.CharField(blank=True, max_length=50, verbose_name='Sangue')),
                ('brincos_cabra', models.CharField(max_length=50, verbose_name='Brincos')),
                ('chifres_cabra', models.BooleanField(verbose_name='Chifres')),
                ('observacao_cabra', models.TextField(blank=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Cabra',
            },
        ),
        migrations.CreateModel(
            name='Cobertura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_cobertura', models.DateField(blank=True, default=None, null=True, verbose_name='Data')),
                ('id_bode', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Bode', verbose_name='Bode')),
                ('id_cabra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Cabra', verbose_name='Cabra')),
            ],
            options={
                'verbose_name': 'Cobertura',
            },
        ),
        migrations.CreateModel(
            name='Fazenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_fazenda', models.CharField(max_length=100, verbose_name='Nome da Fazenda')),
            ],
            options={
                'verbose_name': 'Fazenda',
            },
        ),
        migrations.CreateModel(
            name='Filhote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_filhote', models.IntegerField(verbose_name='Numero')),
                ('peso_filhote', models.DecimalField(decimal_places=4, max_digits=5, verbose_name='Peso')),
                ('sexo_filhote', models.CharField(blank=True, max_length=50, verbose_name='Sexo')),
                ('reposicao_filhote', models.BooleanField(verbose_name='Reposição')),
            ],
            options={
                'verbose_name': 'Filhote',
            },
        ),
        migrations.CreateModel(
            name='Filiacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Filiacao',
            },
        ),
        migrations.CreateModel(
            name='Medicacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Medicacao',
            },
        ),
        migrations.CreateModel(
            name='Parto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_parto', models.DateField(verbose_name='Data')),
                ('observacao_parto', models.TextField(blank=True, verbose_name='Observação')),
                ('id_cobertura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Cobertura', verbose_name='Cobertura')),
            ],
            options={
                'verbose_name': 'Parto',
            },
        ),
        migrations.CreateModel(
            name='Producao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_producao', models.DateTimeField(verbose_name='Data')),
                ('peso_producao', models.DecimalField(decimal_places=4, max_digits=5, verbose_name='Peso')),
                ('id_cabra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Cabra', verbose_name='Cabra')),
            ],
            options={
                'verbose_name': 'Producao',
            },
        ),
        migrations.CreateModel(
            name='Vacina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Vacina',
            },
        ),
        migrations.AddField(
            model_name='filhote',
            name='id_parto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Parto', verbose_name='Parto'),
        ),
        migrations.AddField(
            model_name='cabra',
            name='id_fazenda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Fazenda', verbose_name='Fazenda'),
        ),
        migrations.AddField(
            model_name='bode',
            name='id_fazenda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='animais.Fazenda', verbose_name='Fazenda'),
        ),
    ]
