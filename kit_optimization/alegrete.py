import numpy as np


def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    resultado = 0
    for n in range(len(data)):
        resultado += (theta_0 + theta_1 * data[n,0] - data[n,1])**2
    return resultado/(len(data))

def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    derivada_theta_0 = 0
    derivada_theta_1 = 0

    for n in range(len(data)):
        derivada_theta_0 += (((theta_0 + theta_1 * data[n,0] - data[n,1])*2)/len(data))
        derivada_theta_1 += ((((theta_0 + theta_1 * data[n,0] - data[n,1])*data[n,0])*2)/len(data))
    theta_0 = theta_0 - alpha * derivada_theta_0
    theta_1 = theta_1 - alpha * derivada_theta_1

    return theta_0,theta_1

def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    list_theta_0 = []
    list_theta_1 = []

    for i in range(num_iterations):
        theta_0_aux, theta_1_aux = step_gradient(theta_0, theta_1, data, alpha)
        list_theta_0.append(theta_0_aux)
        list_theta_1.append(theta_1_aux)
    
    return list_theta_0, list_theta_1

