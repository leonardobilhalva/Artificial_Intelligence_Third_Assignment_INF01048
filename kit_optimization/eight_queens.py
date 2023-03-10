import numpy as np
import random
import matplotlib.pyplot as plt


def pega_maior_valor(lista):
    lista_aux = lista.copy()
    individuo_atual = lista_aux.pop(0)
    maior_ataque = evaluate(individuo_atual)

    while(len(lista_aux) > 0):
        individuo_aux = lista_aux.pop(0)
        maior_ataque_aux = evaluate(individuo_aux)

        if maior_ataque_aux > maior_ataque:
            maior_ataque = maior_ataque_aux
            individuo_atual = individuo_aux

    return maior_ataque


def pega_media(lista):
    lista_aux = lista.copy()
    individuo_atual = lista_aux.pop(0)
    valor = evaluate(individuo_atual)
    contador = 1

    while(len(lista_aux) > 0):
        individuo_atual = lista_aux.pop(0)
        valor += evaluate(individuo_atual)
        contador += 1

    return valor/contador


def gera_grafico(maiores_valores, menores_valores, media_valores):
    lista = []
    for i in range(len(maiores_valores)):
        lista.append(i + 1)

    plt.plot(lista, maiores_valores, color='blue')
    plt.plot(lista, menores_valores, color='red')
    plt.plot(lista, media_valores, color='black')

    plt.xlabel("generations")
    plt.ylabel("fitness score")
    plt.savefig('ga.png', format='png')
    plt.show()


def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    ataques = 0
    for i in range(8):
        for j in range(i+1, 8):
            distancia = j - i
            if individual[i] == individual[j]:
                ataques += 1
            elif individual[i] == individual[j] + distancia:
                ataques += 1
            elif individual[i] == individual[j] - distancia:
                ataques += 1
    return ataques


def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    participants_aux = participants.copy()
    individuo_atual = participants_aux.pop(0)
    menor_ataque = evaluate(individuo_atual)

    while(len(participants_aux) > 0):
        individuo_aux = participants_aux.pop(0)
        menor_ataque_aux = evaluate(individuo_aux)

        if menor_ataque_aux < menor_ataque:
            menor_ataque = menor_ataque_aux
            individuo_atual = individuo_aux

    return individuo_atual


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    while(index < 8):
        aux = parent1[index]
        parent1[index] = parent2[index]
        parent2[index] = aux
        index += 1
    return parent1, parent2


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m: - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random.uniform(0, 1.1) < m:
        i = random.randint(0, 7)
        individual[i] = random.randint(1, 8)
    return individual


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    lista_individuos = []
    aux = n
    while(n > 0):
        individuo_aleatorio = np.random.randint(low=1, high=9, size=8).tolist()
        lista_individuos.append(individuo_aleatorio)
        n -= 1

    n = aux

    maiores_valores = []
    menores_valores = []
    media_valores = []

    for i in range(g):
        lista_aux = []

        if(e > 1):
            for j in range(e):
                lista_aux.append(tournament(
                    random.sample(lista_individuos, k)))
        elif(e == 1):
            lista_aux.append(tournament(lista_individuos))

        while(len(lista_aux) < n):
            l1 = random.sample(lista_individuos, k)
            l2 = random.sample(lista_individuos, k)
            p1 = tournament(l1)
            p2 = tournament(l2)
            o1, o2 = crossover(p1, p2, random.randint(0, 8))
            o1 = mutate(o1, m)
            o2 = mutate(o2, m)
            lista_aux.extend([o1, o2])
        lista_individuos = lista_aux

        # gera grafico
        #maiores_valores.append(pega_maior_valor(lista_individuos))
        #menores_valores.append(evaluate(tournament(lista_individuos)))
        #media_valores.append(pega_media(lista_individuos))

    #gera_grafico(maiores_valores, menores_valores, media_valores)
    return tournament(lista_individuos)

run_ga(50, 150, 5, 0, 5)
