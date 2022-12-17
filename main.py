import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#importação de todas as funções dos ficheiros Funçoes e Plots, para que possam ser chamadas neste ficheiro main
from Plots import *

#Leitura de base de dados
diabetes = pd.read_csv("diabetes.csv")
diabetesdf=pd.DataFrame(diabetes)
variaveis = diabetes.columns

"""
adicionar nova coluna na data frame
glucose medida em período pós pradial , 2h após refeição
https://www.mayoclinic.org/tests-procedures/glucose-tolerance-test/about/pac-20394296
até 70mg/dL - hipoglicemia
70 a 140 mg/dL - normal
140 a 200 mg/dL - pré-diabetes
mais de 200 mg/dL - diabetes
"""

#Criação da nova variável categoria tendo em conta os valores de glicemia
x=[]
for i in diabetes["Glucose"]:
    valor = ""
    if i<=70:
        valor= "Hypoglycemia"
    elif i<=140:
        valor= "Normal"
    elif i<=199:
        valor= "Pre-diabetes"
    else:
        valor= "Diabetes"
    x.append(valor)

#Adição da nova variável à base de dados
diabetes.insert(loc=2, column="GlycemiaValues", value=x)
#print(diabetes)

hist_vcat(diabetesdf,"GlycemiaValues")

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
    else:
        exit()


def menu():
    print("  [Menu] Escolhe uma das seguintes opções:")
    print("|     0 - Visualização da DataFrame Diabetes   |")
    print("|     1 - Variables - individual                           |")
    print("|     2 - Variables - all                           |")
    print("|     3 - Interaction and Correlations         |")
    print("|     4 - Report                               |")
    print("|     5 - Sair                                 |")
    opcoes_menu()

#opção 0 - visualização da data frame e de algumas informações relativas à mesma
def opcoes_menu():
    opcao= int(input("Opção:"))
    while opcao < 0 and opcao >= 4:
        print("Tem de escolher uma opção entre 0 e 4")
        menu()
    
    if opcao == 0:
        print(f"Base de Dados Diabetes:\n {diabetesdf}")
        print(f"Informações gerais sobre a base de dados:\n {diabetesdf.info()}")
        opcaoa= int(input("Pretende ainda visualizar:\n 0- Tabela com as primeiras 20 observações \n 1- Tabela com medidas estatísticas das variáveis \n 2- Voltar ao Menu Principal \n Opção:"))
        if opcaoa==0:
            print(f"Tabela com as primeiras 20 observações da base de dados\n {tabelas(diabetesdf,1)}")
            terminar()
        elif opcaoa==1:
            print(f"Tabela com as medidas estatísticas das variáveis \n {tabelas(diabetesdf,2)}")
            terminar()
        else:
            menu()
    
    elif opcao == 1:
        print("            1: Pregnancies                    ")
        print("            2: Glucose                        ")
        print("            3: GlycemiaValues                 ")
        print("            4: BloodPressure                  ")
        print("            5: SkinThickness                  ")
        print("            6: Insulin                        ")
        print("            7: BMI                            ")
        print("            8: DiabetesPedigreeFunction       ")
        print("            9: Age                            ")
        print("            10: Outcome                       ")
        variavel= input(f"Escolha a variável que deseja analisar:")

        outc_values(diabetesdf, vcategorical)
        circular(diabetesdf, vcategorical)
        hist_vcat(diabetesdf, vcategorical)
        var_num(diabetesdf, variavel)
        swarmplotvar(diabetesdf,variavel,vcategorical=None)

    
    #elif opcao == 2:
    #    função3
    
    #elif opcao == 3:
    #    função4
    
    elif opcao == 4:
        #geração de um relatório automático sobre a analise da base de dados
        relatorio = ProfileReport(diabetesdf, title="Data Analysis of Diabetes Report")
        diabetesdf.profile_report()
        relatorio.to_file("diabetes_report.html")
    
    elif opcao == 5:
        exit()
    #else:

menu()

