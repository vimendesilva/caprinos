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
from sklearn.metrics import r2_score, explained_variance_score
from sklearn import preprocessing

from django.shortcuts import render

from django.db import connection

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

    current_date = float(lista[0][4])
    current_month = float(lista[0][5])

    for i in range (len(lista)): # procurar em todas as listas internas
        for j in range (len(lista[i])): # procurar em todos os elementos nessa lista
            if(j == 4):
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
                lista[i][j] = round(float(lista[i][j]), 5)
            # break # saímos do strftime("%m", data_producao)loop interno
        # break # e do externo
    return lista 

@login_required
def MontaDados(request):
    #pega mãe e pai?
    #falta dados meteorológicos
    # cabras = Producao.objects.raw('select animais_animal.id, brincos_animal, raca_animal_id, sangue_animal_id, nascimento_animal, manha_producao, tarde_producao, (manha_producao + tarde_producao) as total from animais_producao'+
    #                             ' inner join animais_animal on animais_animal.id = animais_producao.id_cabra_id')

    cursor = connection.cursor()
    cursor.execute('SELECT total FROM dados')
    total_prod = listfetchall(cursor)
    # print('Prod sem norma')
    # pprint(total_prod)

    total_prod = pd.DataFrame(total_prod)
    mm_scaler = preprocessing.MinMaxScaler()
    y_scaled = mm_scaler.fit_transform(total_prod)
    y_prod = pd.DataFrame(y_scaled)
    y_prod = y_prod.values.tolist()
    # print('Prod com norma')
    # pprint(y_prod)
    # pprint(x_scaled)

    data_atual = date.today()

    cursor = connection.cursor()
    cursor.execute('SELECT raca_animal_id, sangue_animal_id, MONTH(data_producao), DATEDIFF(data_producao, nascimento_animal), DATEDIFF(NOW(), data_producao), MONTH(data_producao) FROM dados')
    # cursor.execute('SELECT raca_animal_id, sangue_animal_id, strftime("%m", data_producao), julianday(data_producao) - julianday(nascimento_animal), julianday(data_producao), strftime("%m", data_producao) FROM dados')
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

    desempenho = explained_variance_score(y_prod[5001:5100], resultado)
    # print('Desempenho')
    # print(desempenho)

    # pprint(y_prod)

    # pprint(resultado)

    dados = {
        'resultado': resultado,
        'x': x_atributos[5001:5100],
        'y': y_prod[5001:5100],
        'soma_y': y_scaled[5001:5100].sum(),
        'soma_r': sum(resultado),
        'desempenho': desempenho,
        'min': resultado.min(),
        'max': resultado.max(),
        'mean': resultado.mean()
    }

    return render(request, 'rede/dados.html', dados)

@login_required
def MLP(request, x_atributos, y_prod):
    
    # To see an example where output falls outside of the range of y
    np.random.seed(1)

    # Create the default NN as you did
    nn = MLPRegressor(
        solver='sgd',
        hidden_layer_sizes=1000,
        max_iter=10000,
        shuffle=False,
        random_state=9876,
        activation='logistic',
        n_iter_no_change=1000,
        learning_rate='constant',
        learning_rate_init=0.00001
        
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
    nn.fit(x_atributos[0:5000], y_prod[0:5000])

    # print('*** Before scaling the output via final activation:\n')

    # Now see that the output activation is (by default) simply linear i.e. 'identity'
    # print('Output activation by default: {}'.format(nn.out_activation_))
    predictions = nn.predict(x_atributos[5001:5100])

    print(nn.loss_)
    print(nn.coefs_)
    print(nn.intercepts_)
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