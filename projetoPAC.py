import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

print("Projeto de PAC - Base de dados 'Diabetes'")

#ler o ficheiro csv
diabetes = pd.read_csv("diabetes.csv")

#transformar em dataframe
diabetesdf=pd.DataFrame(diabetes)
print(diabetesdf)
print(diabetesdf.columns)

"""
adicionar nova coluna na data frame
glucose medida em período pós pradial , 2h após refeição
https://www.mayoclinic.org/tests-procedures/glucose-tolerance-test/about/pac-20394296
até 70mg/dL - hipoglicemia
70 a 140 mg/dL - normal
140 a 200 mg/dL - pré-diabetes
mais de 200 mg/dL - diabetes
"""

x=[]

for i in diabetesdf["Glucose"]:
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

diabetesdf.insert(loc=2, column="GlycemiaValues", value=x)
print(diabetesdf)
#Vai ser adicionada uma nova coluna que vai converter os valores de glucose em 4 patamares

#informações acerca da base de dados (colunas, NA, tipo de variavel, etc)
diabetesdf.info()

########### Opções do utilizador ##########
def printMenu():
    print("-------------------------------------------------------")
    print("|                  0 - Overview                       |")
    print("|                  1 - Variables                      |")
    print("|                  2 - Interaction                    |")
    print("|                  3 - Correlations                   |")
    print("|                  4 - Missing Values                 |")
    print("|                  5 - Sample                         |")
    print("|                  6 - Report                         |")
    print("-------------------------------------------------------")

printMenu()
opcao = int(input("Escolha uma das opções:"))

#opcao= int(input("Escolha uma categoria para a análise que pretende \n 0-Overview \n 1-Variables \n 2-Interaction \n 3-Correlations \n 4-Missing Values \n 5-Sample \n 6-Report \n Opção:  "))
while opcao < 0 and opcao >= 6:
    print("Tem de escolher uma opção entre 0 e 6")
    printMenu()
    opcao = int(input("Escolha uma das opções:"))
    #opcao= int(input("Escolha a opção que deseja \n 0-Overview \n 1-Variables \n 2-Interaction \n 3-Correlations \n 4-Missing Values \n 5-Sample \n 6-Report \n Opção:  "))

#opção 0 - visualização da data frame e de algumas informações relativas à mesma
if opcao == 0:
    print(diabetesdf)
    diabetesdf.info()
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
elif opcao == 6:
    #geração de um relatório automático sobre a analise da base de dados
    relatorio = ProfileReport(diabetesdf, title="Data Analysis of Diabetes Report")
    diabetesdf.profile_report()
    relatorio.to_file("diabetes_report.html")
#else:
