import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px

#importação de todas as funções dos ficheiros Funçoes e Plots, para que possam ser chamadas neste ficheiro main
from Plots import *
from Funçoes import *

def menu():
    print("        [Menu] Escolhe uma das seguintes opções:")
    print("|                  0 - Visualização da DataFrame Diabetes                       |")
    print("|                  1 - Variables                      |")
    print("|                  2 - Interaction                    |")
    print("|                  3 - Correlations                   |")
    print("|                  4 - Sample                         |")
    print("|                  5 - Report                         |")
    print("|                  6 - Sair                         |")
    opcoes_menu()

#opção 0 - visualização da data frame e de algumas informações relativas à mesma
def opcoes_menu():
    opcao= int(input("Opção:"))
    while opcao < 0 and opcao >= 6:
        print("Tem de escolher uma opção entre 0 e 6")
        menu()
    
    if opcao == 0:
        print(f"Base de Dados Diabetes:\n {diabetesdf}")
        print(f"Informações gerais sobre a base de dados:\n {diabetesdf.info()}")
        opcaoa= int(input("Pretende ainda visualizar:\n 0- tabela com as primeiras 20 observações \n 1- tabela com cálculos estatísticos das variáveis \n 2-Voltar ao Menu Principal \n Opção:"))
        if opcaoa==0:
            print(f"Tabela com as primeiras 20 observações da base de dados\n {tabelas(diabetesdf,1)}")
            terminar()
        elif opcaoa==1:
            print(f"Tabela com as primeiras 20 observações da base de dados\n {tabelas(diabetesdf,2)}")
            terminar()
        else:
            exit()
        menu()
    
    elif opcao == 1:
        variavel= int(input("Escolha uma das seguintes opções:\n 0-Análise Geral das Variáveis Numéricas \n 1- "))
        if variavel==0:
            print(diabetesdf.describe())
        elif variavel==1:
            print("xau")
    
    #elif opcao == 2:
    #    função3
    
    #elif opcao == 3:
    #    função4
    
    elif opcao == 5:
        #geração de um relatório automático sobre a analise da base de dados
        relatorio = ProfileReport(diabetesdf, title="Data Analysis of Diabetes Report")
        diabetesdf.profile_report()
        relatorio.to_file("diabetes_report.html")
    
    elif opcao == 6:
        exit()
    #else:

menu()

#função para todos os fins de opção perguntar se quer continuar ou terminar a analise
def terminar():
    escolha=input("Deseja continuar a análise estatística? Escreva 'Sim' para continuar ou 'Não' para terminar \n")
    escolha = escolha.lower()
    while escolha != "sim" and escolha != "s" and escolha != "não" and escolha != "n" and escolha != "nao":
        print("Resposta inválida. Escreva 'Sim' para continuar a análise e 'Não' para terminar. \n")
        escolha=input("Deseja continuar a análise estatística? Escreva 'Sim' para continuar ou 'Não' para terminar \n")
        escolha = escolha.lower()

    if escolha == "sim" or escolha == "s":
        menu()
    elif escolha == "Não":
        exit()