from pprint import pprint
import datetime
from datetime import date
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from weasyprint import HTML

from caprino.animais.models import *

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error, mean_absolute_error, mean_squared_log_error, median_absolute_error, accuracy_score
from sklearn import preprocessing

from django.shortcuts import render

from django.db import connection

import random
import pandas as pd
import numpy as np

def listfetchall(cursor):
    "Return all rows from a cursor as a list"
    columns = [col[0] for col in cursor.description]
    return [float(row[0]) for row in cursor.fetchall()]

def matrixfetchall(cursor):
    "Return all rows from a cursor as a matrix"

    columns = [col[0] for col in cursor.description]
    lista = [list(row) for row in cursor.fetchall()]

    current_date = float(lista[0][3])
    current_month = float(lista[0][4])

    for i in range (len(lista)): # procurar em todas as listas internas
        for j in range (len(lista[i])): # procurar em todos os elementos nessa lista
            if(j == 3):
                if i < len(lista) -1:
                    today = lista[i][j]
                    tomorrow = lista[i+1][j]

                    if (abs(today - tomorrow) <= 1):
                        lista[i][j] = lista[i][j] - current_date
                        lista[i][j+1] = current_month
                    else:
                        lista[i][j] = lista[i][j] - current_date
                        lista[i][j+1] = current_month
                        current_date = float(lista[i+1][j])
                        current_month = float(lista[i+1][j+1])
                else:
                    lista[i][j] = lista[i][j] - current_date
            else:
                lista[i][j] = round(float(lista[i][j]), 1)
            # break # saímos do strftime("%m", data_producao)loop interno
        # break # e do externo
    return lista 

@login_required
def EscolheRede(request):
    animais = Animal.objects.all().filter(sexo_animal=2).filter(vida_animal=2)
    return render(request, 'rede/escolha_rede.html', {'animais': animais})

@login_required
def MontaDados(request):

    if(request.method == 'POST'):
        # print(request.POST)
        data = request.POST.get('data')
        cabras = json.loads(request.POST.get('cabras'))
        print(data)
        print(len(cabras))

        # INICIO TREINO #

        cursor = connection.cursor()
        cursor.execute('SELECT total FROM dados')
        total_prod = listfetchall(cursor)
        
        total_prod = pd.DataFrame(total_prod)
        mm_scaler = preprocessing.MinMaxScaler()
        y_scaled = mm_scaler.fit_transform(total_prod)
        y_prod = pd.DataFrame(y_scaled)
        y_prod = y_prod.values.tolist()
        y_prod = [x[0] for x in y_prod]
        

        cursor = connection.cursor()
        # cursor.execute('SELECT raca_animal_id, MONTH(data_producao), DATEDIFF(data_producao, nascimento_animal), DATEDIFF(NOW(), data_producao), MONTH(data_producao) FROM dados')
        cursor.execute('SELECT raca_animal_id, strftime("%m", data_producao), julianday(data_producao) - julianday(nascimento_animal), julianday(data_producao), strftime("%m", data_producao) FROM dados')
        outros = matrixfetchall(cursor)

        out = pd.DataFrame(outros)
        mm_scaler = preprocessing.MinMaxScaler()
        x_scaled = mm_scaler.fit_transform(out)
        x_atributos = pd.DataFrame(x_scaled)
        x_atributos = x_atributos.values.tolist()

        # # FIM TREINO #

        # # INICIO TESTE #

        cursor = connection.cursor()
        cursor.execute('SELECT total FROM dados WHERE data_producao = "' + str(data) + '"')
        prod = listfetchall(cursor)
        print('Prod sem norma')
        pprint(total_prod)

        prod = pd.DataFrame(prod)
        mm_scaler = preprocessing.MinMaxScaler()
        y_scaled = mm_scaler.fit_transform(prod)
        teste_prod = pd.DataFrame(y_scaled)
        teste_prod = teste_prod.values.tolist()
        teste_prod = [x[0] for x in teste_prod]

        cursor = connection.cursor()
        # cursor.execute('SELECT raca_animal_id, MONTH(data_producao), DATEDIFF(data_producao, nascimento_animal), DATEDIFF(NOW(), data_producao), MONTH(data_producao) FROM dados')
        cursor.execute('SELECT raca_animal_id, strftime("%m", data_producao), julianday(data_producao) - julianday(nascimento_animal), julianday(data_producao), strftime("%m", data_producao) FROM dados WHERE data_producao = "' + str(data) + '"')
        teste = matrixfetchall(cursor)

        teste = pd.DataFrame(teste)
        mm_scaler = preprocessing.MinMaxScaler()
        x_scaled = mm_scaler.fit_transform(teste)
        teste_outros = pd.DataFrame(x_scaled)
        teste_outros = teste_outros.values.tolist()

        # # FIM TESTE #

        resultado = MLP_Predicao(request, teste_outros, y_prod, x_atributos)

        desempenho = explained_variance_score(y_prod, resultado)
        me = mean_squared_error(teste_prod, resultado)

        grafico = {
            'teste': teste_prod,
            'resultado': resultado.tolist()
        }

        dados = {
        'grafico': json.dumps(grafico),
        'resultado': resultado,
        # 'x': x_atributos[5001:5100],
        'y': teste_prod,
        'soma_y': y_scaled.sum(),
        'soma_r': sum(resultado),
        'desempenho': desempenho,
        'me': me,
        'min': resultado.min(),
        'max': resultado.max(),
        'mean': resultado.mean()
        }

    #pega mãe e pai?
    #falta dados meteorológicos
    # cabras = Producao.objects.raw('select animais_animal.id, brincos_animal, raca_animal_id, sangue_animal_id, nascimento_animal, manha_producao, tarde_producao, (manha_producao + tarde_producao) as total from animais_producao'+
    #                             ' inner join animais_animal on animais_animal.id = animais_producao.id_cabra_id')
    else:
        cursor = connection.cursor()
        cursor.execute('SELECT total FROM dados order by data_producao')
        total_prod = listfetchall(cursor)
        print('Prod sem norma')
        pprint(total_prod)

        total_prod = pd.DataFrame(total_prod)
        mm_scaler = preprocessing.MinMaxScaler()
        y_scaled = mm_scaler.fit_transform(total_prod)
        y_prod = pd.DataFrame(y_scaled)
        y_prod = y_prod.values.tolist()
        y_prod = [x[0] for x in y_prod]
        # print('Prod com norma')
        # pprint(y_prod)
        # pprint(x_scaled)

        data_atual = date.today()

        cursor = connection.cursor()
        cursor.execute('SELECT raca_animal_id, MONTH(data_producao), DATEDIFF(data_producao, nascimento_animal), DATEDIFF(NOW(), data_producao), MONTH(data_producao), total FROM dados')
        # cursor.execute('SELECT raca_animal_id, strftime("%m", data_producao), julianday(data_producao) - julianday(nascimento_animal), julianday(data_producao), strftime("%m", data_producao), media-1 FROM dados order by data_producao')
        outros = matrixfetchall(cursor)
        print('Outros sem norma')
        pprint(outros)

        out = pd.DataFrame(outros)
        mm_scaler = preprocessing.MinMaxScaler()
        x_scaled = mm_scaler.fit_transform(out)
        x_atributos = pd.DataFrame(x_scaled)
        x_atributos = x_atributos.values.tolist()
        # print('Outros com norma')
        # pprint(x_atributos)

        # pprint(out)

        resultado = MLP(request, x_atributos, y_prod)

        inicio_treino = 0
        final_treino = 3000
        inicio_teste = 3001
        final_teste = 5000

        evs = explained_variance_score(y_prod[inicio_teste:final_teste], resultado)
        mse = mean_squared_error(y_prod[inicio_teste:final_teste], resultado)
        mean_ae = mean_absolute_error(y_prod[inicio_teste:final_teste], resultado)
        # msle = mean_squared_log_error(y_prod[inicio_teste:final_teste], resultado)
        median_ae = median_absolute_error(y_prod[inicio_teste:final_teste], resultado)
        # a_score = accuracy_score(y_prod[inicio_teste:final_teste], resultado)
        r2 = r2_score(y_prod[inicio_teste:final_teste], resultado)
        
        grafico = {
            'teste': y_prod[inicio_teste:final_teste],
            'resultado': resultado.tolist()
        }

        # pprint(grafico)

        dados = {
            'grafico': json.dumps(grafico),
            'resultado': resultado,
            # 'x': x_atributos[5001:5100],
            'y': y_prod[inicio_teste:final_teste],
            'soma_y': y_scaled[inicio_teste:final_teste].sum(),
            'soma_r': sum(resultado),
            'evs': evs,
            'mse': mse,
            'mean_ae': mean_ae,
            # 'msle': msle,
            'median_ae': median_ae,
            'r2': r2,
            # 'a_score': a_score,
            'min': resultado.min(),
            'max': resultado.max(),
            'mean': resultado.mean()
        }
    # print(dados)
    return render(request, 'rede/dados.html', dados)

@login_required
def MLP(request, x_atributos, y_prod):
    inicio_treino = 0
    final_treino = 3000
    inicio_teste = 3001
    final_teste = 5000

    # Create the default NN as you did
    nn = MLPRegressor(
        hidden_layer_sizes=(100, 100, 100, 100),
        alpha=0,
        activation='tanh',
        solver='sgd',
        max_iter=10000,
        n_iter_no_change=1000
        
        
        # solver='sgd',
        # hidden_layer_sizes=1000,
        # max_iter=10000,
        # shuffle=True,
        # activation='tanh',
        # n_iter_no_change=1000,
        # learning_rate='adaptive',
        # alpha=0.001

    #     hidden_layer_sizes=(1000,),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
    # learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=10000, shuffle=True,
    # random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
    # early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08
        
        # hidden_layer_sizes=1000, 
        # activation='relu', 
        # solver='adam', 
        # alpha=0.0000001, 
        # batch_size='auto', 
        # learning_rate='constant', 
        # learning_rate_init=0.00000001, 
        # power_t=0.5, 
        # max_iter=10000, 
        # shuffle=True, 
        # random_state=None, 
        # tol=0.000000001, 
        # verbose=False, 
        # warm_start=False, 
        # momentum=0.9, 
        # nesterovs_momentum=True, 
        # early_stopping=False, 
        # validation_fraction=0.00001, 
        # beta_1=0.9, 
        # beta_2=0.999, 
        # epsilon=1e-08, 
        # n_iter_no_change=1000
        )

    # Fit the network
    nn.fit(x_atributos[inicio_treino:final_treino], y_prod[inicio_treino:final_treino])
    # nn.out_activation_ = 'tanh'

    # print('*** Before scaling the output via final activation:\n')

    # Now see that the output activation is (by default) simply linear i.e. 'identity'
    # print('Output activation by default: {}'.format(nn.out_activation_))
    nn.predict(x_atributos[3001:4999])
    predictions = nn.predict(x_atributos[inicio_teste:final_teste])
    print(nn.score(x_atributos[inicio_treino:final_treino], y_prod[inicio_treino:final_treino]))
    print(nn.loss_)
    # print(nn.coefs_)
    # print(nn.intercepts_)
    print(nn.n_iter_)
    print(nn.n_layers_)
    print(nn.n_outputs_)
    print(nn.out_activation_)

    # print('Prediction mean: {:.2f}'.format(predictions.mean()))
    # print('Prediction max: {:.2f}'.format(predictions.max()))
    # print('Prediction min: {:.2f}'.format(predictions.min()))

    # print('\n*** After scaling the output via final activation:\n')

    # # Need to recreate the NN
    # nn_logistic = MLPRegressor(
    #     solver='lbfgs',
    #     hidden_layer_sizes=50,
    #     max_iter=10000,
    #     shuffle=False,
    #     random_state=9876,
    #     activation='relu')

    # # Fit the new network
    # nn_logistic.fit(x_atributos, y_prod)


    # # --------------- #
    # #  Crucial step!  #
    # # --------------- #

    # # before making predictions = alter the attribute: "output_activation_"
    # nn_logistic.out_activation_ = 'logistic'
    # print('New output activation: {}'.format(nn_logistic.out_activation_))

    # new_predictions = nn_logistic.predict(lista_teste)

    # print('Prediction mean: {:.2f}'.format(new_predictions.mean()))
    # print('Prediction max: {:.2f}'.format(new_predictions.max()))
    # print('Prediction min: {:.2f}'.format(new_predictions.min()))

    return(predictions)


@login_required
def MLP_Predicao(request, teste, y_prod, x_atributos):
    
    # To see an example where output falls outside of the range of y
    np.random.seed(1)

    # Create the default NN as you did
    nn = MLPRegressor(
        hidden_layer_sizes=(100, 100, 100, 100),
        alpha=0,
        activation='tanh',
        solver='sgd',
        max_iter=10000,
        n_iter_no_change=1000 
    )

    # Fit the network
    nn.fit(x_atributos, y_prod)
    # nn.out_activation_ = 'relu'

    predictions = nn.predict(teste)

    print(nn.loss_)
    # print(nn.coefs_)
    # print(nn.intercepts_)
    print(nn.n_iter_)
    print(nn.n_layers_)
    print(nn.n_outputs_)
    print(nn.out_activation_)


    return(predictions)