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
    for i in range (len(lista)): # procurar em todas as listas internas
        for j in range (i): # procurar em todos os elementos nessa lista
            lista[i][j] = float(lista[i][j])
            break # saímos do loop interno
        break # e do externo
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
    x_scaled = mm_scaler.fit_transform(total_prod)
    y_prod = pd.DataFrame(x_scaled)
    y_prod = y_prod.values.tolist()
    print('Prod com norma')
    pprint(y_prod)
    # pprint(x_scaled)

    data_atual = date.today()

    cursor = connection.cursor()
    # cursor.execute('SELECT raca_animal_id, sangue_animal_id, DATEDIFF(' + str(data_atual) + ', nascimento_animal) FROM dados')
    cursor.execute('SELECT raca_animal_id, sangue_animal_id, (' + str(data_atual) + ' - nascimento_animal) FROM dados')
    outros = matrixfetchall(cursor)
    # print('Outros sem norma')
    # pprint(outros)

    out = pd.DataFrame(outros)
    mm_scaler = preprocessing.MinMaxScaler()
    y_scaled = mm_scaler.fit_transform(out)
    x_atributos = pd.DataFrame(y_scaled)
    x_atributos = x_atributos.values.tolist()
    print('Outros com norma')
    pprint(x_atributos)

    resultado = MLP(request, x_atributos, y_prod)

    return render(request, 'rede/dados.html')

@login_required
def MLP(request, x_atributos, y_prod):
    
    # To see an example where output falls outside of the range of y
    np.random.seed(1)

    # Create the default NN as you did
    nn = MLPRegressor(
        solver='lbfgs',
        hidden_layer_sizes=50,
        max_iter=10000,
        shuffle=False,
        random_state=9876,
        activation='relu')

    lista_teste = [[1.0, 0.8, 0.5],[1.0, 0.2, 0.0],[0.0, 0.0, 0.0]]

    # Fit the network
    nn.fit(x_atributos, y_prod)

    print('*** Before scaling the output via final activation:\n')

    # Now see that the output activation is (by default) simply linear i.e. 'identity'
    print('Output activation by default: {}'.format(nn.out_activation_))
    predictions = nn.predict(lista_teste)

    print('Prediction mean: {:.2f}'.format(predictions.mean()))
    print('Prediction max: {:.2f}'.format(predictions.max()))
    print('Prediction min: {:.2f}'.format(predictions.min()))


    print('\n*** After scaling the output via final activation:\n')

    # Need to recreate the NN
    nn_logistic = MLPRegressor(
        solver='lbfgs',
        hidden_layer_sizes=50,
        max_iter=10000,
        shuffle=False,
        random_state=9876,
        activation='relu')

    # Fit the new network
    nn_logistic.fit(x_atributos, y_prod)


    # --------------- #
    #  Crucial step!  #
    # --------------- #

    # before making predictions = alter the attribute: "output_activation_"
    nn_logistic.out_activation_ = 'logistic'
    print('New output activation: {}'.format(nn_logistic.out_activation_))

    new_predictions = nn_logistic.predict(lista_teste)

    print('Prediction mean: {:.2f}'.format(new_predictions.mean()))
    print('Prediction max: {:.2f}'.format(new_predictions.max()))
    print('Prediction min: {:.2f}'.format(new_predictions.min()))