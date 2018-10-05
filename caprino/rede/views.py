from sklearn.neural_network import MLPRegressor

from django.shortcuts import render

# import pandas as pd
import numpy as np

@login_required
def MontaDados(request):
    #pega mãe e pai?
    #falta dados meteorológicos
    cabras = Animal.objects.raw('select manha_producao, tarde_producao, raca_animal, sangue_animal, nascimento_animal from animais_producao'+
                                'inner join animais_animal on animais_animal.id = animais_producao.id_cabra_id')


@login_required
def MLP(request):
    
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

    # Generate some fake data
    num_train_samples = 50
    num_test_samples = 50
    num_vars = 2

    X = np.random.random((num_train_samples, num_vars)) * \
        100  # random numbers between 0 and 100
    y = np.random.uniform(0, 1, (num_train_samples, 1))  # uniform numbers between 0 and 1

    X_test = np.random.random((num_test_samples, num_vars)) * 100
    y_test = np.random.uniform(0, 1, (num_test_samples, 1))

    # Fit the network
    nn.fit(X, y)

    print('*** Before scaling the output via final activation:\n')

    # Now see that the output activation is (by default) simply linear i.e. 'identity'
    print('Output activation by default: {}'.format(nn.out_activation_))
    predictions = nn.predict(X_test)

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
    nn_logistic.fit(X, y)


    # --------------- #
    #  Crucial step!  #
    # --------------- #

    # before making predictions = alter the attribute: "output_activation_"
    nn_logistic.out_activation_ = 'logistic'
    print('New output activation: {}'.format(nn_logistic.out_activation_))

    new_predictions = nn_logistic.predict(X_test)

    print('Prediction mean: {:.2f}'.format(new_predictions.mean()))
    print('Prediction max: {:.2f}'.format(new_predictions.max()))
    print('Prediction min: {:.2f}'.format(new_predictions.min()))