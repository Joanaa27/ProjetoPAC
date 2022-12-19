import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#importação de todas as funções dos ficheiros Funçoes e Plots, para que possam ser chamadas neste ficheiro main
from Plots import *

#Leitura de base de dados
diabetes = pd.read_csv("diabetes.csv")
diabetesdf = pd.DataFrame(diabetes)
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
    if i <= 70:
        valor = "Hypoglycemia"
    elif i <= 140:
        valor = "Normal"
    elif i <= 199:
        valor = "Pre-diabetes"
    else:
        valor = "Diabetes"
    x.append(valor)

#Adição da nova variável à base de dados
diabetes.insert(loc = 2, column = "GlycemiaValues", value = x)
#print(diabetes)

###FUNÇÕES###

#função para todos os fins de opção perguntar se quer continuar ou terminar a analise
def terminar():
    escolha = input("Deseja continuar a análise estatística? Escreva 'Sim' para continuar ou 'Não' para terminar \n")
    escolha = escolha.lower()

    while escolha not in ("sim" ,"não", "nao", "s","n"):
        print("Resposta inválida. Escreva 'Sim' para continuar a análise e 'Não' para terminar. \n")
        escolha=input("Deseja continuar a análise estatística? Escreva 'Sim' para continuar ou 'Não' para terminar \n")
        escolha = escolha.lower()

    if escolha in ("sim" ,"s"):
        menu()
    else:
        exit()

def menu():
    print("[Menu] Escolhe uma das seguintes opções:")
    print("     0 - Visualização da base de dados")
    print("     1 - Análise individual de variáveis numéricas")
    print("     2 - Análise individual de variáveis categóricas")
    print("     3 - Análise conjunta de variáveis")
    print("     4 - Interações e Correlações entre as variáveis")
    print("     5 - Cálculos das medidas amostrais das variáveis")
    print("     6 - Relatório geral da base de dados")
    print("     7 - Sair")
    opcoes_menu()

def menu_opcao():
    print("            0: Pregnancies                    ")
    print("            1: Glucose                        ")
    print("            2: BloodPressure                  ")
    print("            3: SkinThickness                  ")
    print("            4: Insulin                        ")
    print("            5: BMI                            ")
    print("            6: DiabetesPedigreeFunction       ")
    print("            7: Age                            ")

def menu_opcao1b():
    def print_menu_opcao1b():
        print("           0: Representação estatística e gráfica     ")
        print("           1: Swarmplot                               ")
        print("           2: Histograma com função densidade         ")

    print_menu_opcao1b()
    escolha2=int(input("       Escolha o gráfico que pretende visualizar:     "))
    while escolha2 not in (1,2,0):
        print("Resposta Inválida.")
        print_menu_opcao1b()
        escolha2=int(input("       Escolha o gráfico que pretende visualizar:     "))
    return escolha2

def menu_opcao2():
    def print_menu_opcao2():
        print("G: GlycemiaValues")
        print("O: Outcome")
    print_menu_opcao2()
    escolha3=input("Escolha a variável que pretende analisar, do menu acima:  ")
    escolha3=escolha3.lower()
    while escolha3 not in ("g","o"):
        print("Resposta inválida.")
        print_menu_opcao2()
        escolha3=input("Escolha a variável que pretende analisar, do menu acima:  ")
    return escolha3

def menu_categoricas():
    def print_menu_2b():
        print("0: Gráfico de Barras")
        print("1: Gráfico Circular")
    print_menu_2b()
    escolha3b=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    while escolha3b not in (0,1):
        print("Resposta inválida.")
        print_menu_2b()
        escolha3b=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    return escolha3b

def menu_3():
    def print_menu3():
        print("    0: Boxplot                            ")
        print("    1: Stripplot                          ")
        print("    2: Pairplot                           ")
        print("    3: Histograma + Função densidade      ")
    print_menu3()
    escolha4=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    while escolha4 not in (0,1,2,3):
        print("Resposta inválida.")
        print_menu3()
        escolha4=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    return escolha4

def get_lista_variaveis():
    dict_variaveis={0: "Pregnancies", 1: "Glucose", 2: "BloodPressure", 3: "SkinThickness", 4: "Insulin", 5: "BMI", 6: "DiabetesPedigreeFunction", 7: "Age"}
    menu_opcao()
    variaveis= int(input("Escolha a variável utilizando os números indicados no menu acima: \n"))
        
    while variaveis <0 or variaveis> 7:
        print("Tem de escolher um número válido, de 0 a 7.")
        variaveis= int(input("Escolha a variável utilizando os números indicados no menu acima: \n"))

    list_variaveis=[]
    if variaveis not in list_variaveis:
        list_variaveis.append(variaveis)
    else:
        print("Esta variável já foi adicionada à lista.")

    escolha= input("Deseja escolher outra variável? Sim ou Não? \n")
    escolha=escolha.lower()
    while escolha not in ("não" ,"n","nao"):
        if escolha in ("sim" , "s"):
            menu_opcao()
            variaveis= int(input("Escolha a variável utilizando os números indicados no menu acima: \n"))
            while variaveis <0 or variaveis> 7:
                print("Tem de escolher um número válido, de 0 a 7.")
                menu_opcao()
                variaveis= int(input("Escolha a variável utilizando os números indicados no menu acima: \n"))
            if variaveis not in list_variaveis:
                list_variaveis.append(variaveis)
            else:
                print("Esta variável já foi adicionada à lista.")
            escolha= input("Deseja escolher outra variável? Sim ou Não? \n")
            escolha=escolha.lower()
        else:
            print("Resposta inválida.")
            escolha=input("Deseja escolher outra variável? Sim ou Não? \n")
            escolha = escolha.lower()

    list_converted=[dict_variaveis.get(v) for v in list_variaveis]
    print(list)
    return list_converted

def varcategorical():
    dict_vcateg={"o":"Outcome","g": "GlycemiaValues","n":None}
    vcategorical = input("Deseja fazer em função da variável Outcome (O), da variável GlycemiaValues (G) ou Nenhuma (N)? \n")
    vcategorical=vcategorical.lower()
    while vcategorical not in ("o" , "g","n"):
        print("Resposta Inválida.")
        vcategorical = input("Deseja fazer em função da variável Outcome (O), da variável GlycemiaValues (G) ou Nenhuma (N)? \n")
    vcategorical = dict_vcateg.get(vcategorical)
    return vcategorical

def categorical_without_n():
    dict_Wnone={"o":"Outcome","g": "GlycemiaValues"}
    vcategorical = input("Deseja fazer em função da variável Outcome (O), da variável GlycemiaValues (G)? \n")
    vcategorical=vcategorical.lower()
    while vcategorical not in ("o" , "g"):
        print("Resposta Inválida.")
        vcategorical = input("Deseja fazer em função da variável Outcome (O), da variável GlycemiaValues (G)? \n")
    vcategorical = dict_Wnone.get(vcategorical)
    return vcategorical

def dropval():
    drop_values=[]
    valores_drop=input("Deseja eliminar alguma variável da análise? Sim ou Não? \n")
    valores_drop=valores_drop.lower()

    while valores_drop not in ("sim" ,"não", "nao", "s","n"):
        print("Resposta inválida.")
        valores_drop=input("Deseja eliminar alguma variável da análise? Sim ou Não? \n")
        valores_drop = valores_drop.lower()

    if valores_drop in ("sim" ,"s"):
        drop_values=get_lista_variaveis()
    
    drop_values.append("GlycemiaValues")
    return drop_values

def outcom():        
    has_outcome=False
    outc=input("Deseja fazer em função da variável 'Outcome'? Sim ou Não?")
    outc=outc.lower()
    
    while outc not in ("sim" ,"não", "nao", "s","n"):
        print("Resposta inválida. Escreva 'Sim' para continuar a análise e 'Não' para terminar. \n")
        outc=input("Deseja fazer em função da variável 'Outcome'? Sim ou Não?")
        outc = outc.lower()
    
    if outc in ("sim" ,"s"):
        has_outcome=True
    
    return has_outcome

def menu_4():
    def print_menu4():
        print("    0: Regressão linear")
        print("    1: Gráficos de dispersão")
        print("    2: Matriz de correlações")
    print_menu4()
    escolha5=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    while escolha5 not in (0,1,2):
        print("Resposta inválida.")
        print_menu4()
        escolha5=int(input("Escolha o gráfico do menu acima que pretende visualizar:  "))
    return escolha5

def variavel():
    dict_variaveis={0: "Pregnancies", 1: "Glucose", 2: "BloodPressure", 3: "SkinThickness", 4: "Insulin", 5: "BMI", 6: "DiabetesPedigreeFunction", 7: "Age"}
    menu_opcao()
    variaveis= int(input("Escolha a variável que deseja analisar utilizando os números indicados no menu acima:"))
        
    while variaveis <0 or variaveis> 7:
        print("Tem de escolher um número válido, de 0 a 7.")
        variaveis= int(input("Escolha a variável que deseja analisar utilizando os números indicados no menu acima:"))

    variavel_x=dict_variaveis.get(variaveis)
    return variavel_x

def menu_5():
    def print_menu5():
        print("    0: Média")
        print("    1: Média Ponderada")
        print("    2: Mediana")
        print("    3: Moda")
        print("    4: Variância")
        print("    5: Desvio Padrão")
        print("    6: Assimetria")

    print_menu5()
    escolha6=int(input("Escolha o cálculo do menu acima que pretende efetuar:  "))
    while escolha6 not in (0,1,2,3,4,5,6):
        print("Resposta inválida.")
        print_menu5()
        escolha6=int(input("Escolha o cálculo do menu acima que pretende efetuar:  "))
    return escolha6

def save_file(calcs_to_write):
    decisao=input("Deseja guardar o cálculo num ficheiro? Sim ou Não? \n")
    decisao = decisao.lower()

    while decisao not in ("sim" ,"não", "nao", "s","n"):
        print("Resposta inválida. Escreva 'Sim' para guardar o cálculo e 'Não' para não guardar. \n")
        decisao=input("Deseja guardar o cálculo num ficheiro? Sim ou Não? \n")
        decisao = decisao.lower()

    if decisao in ("sim" ,"s"):
        nome=input("Escolha o nome do seu ficheiro: ")
        new_file = open(f"{nome}.txt", "w")
        new_file.writelines(calcs_to_write)
        new_file.close()

### MENU ###

#opção 0 - visualização da data frame e de algumas informações relativas à mesma
def opcoes_menu():
    opcao = int(input("Opção:"))
    while opcao < 0 or opcao > 7:
        print("Tem de escolher uma opção entre 0 e 7")
        menu()

    if opcao == 0:
        print(f"Base de Dados Diabetes:\n {diabetesdf}")
        print("Informações gerais sobre a base de dados:\n")
        print(diabetesdf.info())
        opcaoa = int(input("Pretende ainda visualizar:\n 0- Tabela com as primeiras 20 observações \n 1- Tabela com medidas estatísticas das variáveis \n 2- Voltar ao Menu Principal \n Opção:"))
        if opcaoa == 0:
            print(f"Tabela com as primeiras 20 observações da base de dados\n {tabelas(diabetesdf,1)}")
            terminar()
        elif opcaoa == 1:
            print(f"Tabela com as medidas estatísticas das variáveis \n {tabelas(diabetesdf,2)}")
            terminar()
        else:
            menu()
    
    elif opcao == 1:
        list_converted = get_lista_variaveis()
        escolha2 = menu_opcao1b()

        print(list_converted)
        if escolha2==0:
            var_num(diabetesdf, list_converted)
            terminar()
        elif escolha2==1:
            vcategorical = varcategorical()
            swarmplotvar(diabetesdf, list_converted, vcategorical) #damos a opção Outcome ou GlycemiaValues ou sem condicionante
            terminar()   
        elif escolha2==2:
            vcategorical=categorical_without_n()
            hist_vcat(diabetesdf, vcategorical,list_converted) #damos a opção Outcome ou GlycemiaValues
            terminar()

    elif opcao == 2:
        escolha3b=menu_categoricas()
        escolha3=menu_opcao2()
        dict_vcateg={"o":"Outcome","g": "GlycemiaValues","n":None}
        if escolha3b==0:
            if escolha3=="g":
                categorica_values(diabetesdf, dict_vcateg.get(escolha3))
                terminar()
            else:
                categorica_values(diabetesdf, dict_vcateg.get(escolha3))
                terminar()
        else:
            if escolha3=="g":
                circular(diabetesdf, dict_vcateg.get(escolha3))
                terminar()
            else:
                circular(diabetesdf, dict_vcateg.get(escolha3))
                terminar()
                
    elif opcao == 3:
        escolha4=menu_3()

        if escolha4==0:
            drop_values = dropval()
            has_outcome = outcom()
            boxplot_all(diabetesdf, drop_values, has_outcome)
            terminar()
        elif escolha4==1:
            drop_values = dropval()
            has_outcome = outcom()
            stripvar(diabetesdf, drop_values, has_outcome)
            terminar()
        elif escolha4==2:
            vcategorical=varcategorical()
            pairplt(diabetesdf, vcategorical) 
            terminar()
        else:
            has_outcome = outcom()
            hist_total(diabetesdf,has_outcome)
            terminar()
    
    elif opcao == 4:
        escolha5=menu_4()
        if escolha5==0:
            print("Variável do eixo dos xx")
            variavel_1= variavel()
            print("Variável do eixo dos yy")
            variavel_2=variavel()
            while variavel_2 == variavel_1:
                print("As variáveis não podem ser iguais.")
                print("Variável do eixo dos yy")
                variavel_2= variavel()
            vcategorical=varcategorical()
            regressao (diabetesdf, variavel_1, variavel_2, vcategorical)
            terminar()

        elif escolha5==1:
            print("Variável do eixo dos xx")
            variavel_1= variavel()
            print("Variável do eixo dos yy")
            variavel_2=variavel()
            while variavel_2 == variavel_1:
                print("As variáveis não podem ser iguais.")
                print("Variável do eixo dos yy")
                variavel_2= variavel()
            vcategorical=varcategorical()
            scatterplt(diabetesdf, variavel_1, variavel_2, vcategorical)
            terminar()

        else:
            matrcorr(diabetesdf)
            terminar()

    elif opcao == 5:
        lista=get_lista_variaveis()
        escolha6=menu_5()
        if escolha6==0:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Média da variável {c}")
                calc_valor = np.mean(lista_valores).round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Media da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==1:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Média ponderada da variável {c}")
                calc_valor = np.average(lista_valores).round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Media ponderada da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==2:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Mediana da variável {c}")
                calc_valor = np.median(lista_valores).round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Mediana da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==3:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Moda da variável {c}")
                calc_valor = lista_valores.mode.round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Moda da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==4:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Variância da variável {c}")
                calc_valor=np.var(lista_valores).round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Variancia da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==5:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Desvio padrão da variável {c}")
                calc_valor=np.std(lista_valores,ddof=1).round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Desvio padrao da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()
        elif escolha6==6:
            list_calcs_to_write=[]
            for c in lista:
                lista_valores=diabetesdf[c].values
                print(f"Assimetria da variável {c}")
                calc_valor=lista_valores.skew.round(2)
                print(calc_valor)
                list_calcs_to_write.append(f"Assimetria da variavel {c}: {calc_valor} \n")
            save_file(list_calcs_to_write)
            terminar()

    elif opcao == 6:
        #geração de um relatório automático sobre a analise da base de dados
        relatorio = ProfileReport(diabetesdf, title = "Relatório da Análise da Base de Dados Diabetes")
        diabetesdf.profile_report()
        relatorio.to_file("diabetes_report.html")
    
    elif opcao == 7:
        exit()

menu()