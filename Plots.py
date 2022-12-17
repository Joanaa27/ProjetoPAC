#Importação de pacotes
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px

#Leitura de base de dados
diabetes = pd.read_csv("diabetes.csv")
diabetesdf=pd.DataFrame(diabetes)

#Criação da nova variável categoria tendo em conta os valores de glicemia
x=[]
for i in diabetes["Glucose"]:
    valor = ""
    if i<=70:
        valor= "Hypoglycemia"
    elif i>70 and i<=140:
        valor= "Normal"
    elif i>140 and i<=199:
        valor= "Pre-diabetes"
    else:
        valor= "Diabetes"
    x.append(valor)

#Adição da nova variável à base de dados
diabetes.insert(loc=2, column="GlycemiaValues", value=x)
#print(diabetes)

#boxplot de todas as variáveis em função da variavel "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na dataframe
diabetesbp= diabetesdf.drop("GlycemiaValues", axis=1)
diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")

def boxplot_all():
    plt.figure(figsize = (15, 15))
    sns.boxplot(data = diabetes_melted, x="variables", y="value", hue="Outcome")
    plt.title("Boxplot of all numeric variables in order to Outcome")
    plt.show()

#swarm plot de todas as variavem em função da variável "Outcome"
def swarvar():
    plt.figure(figsize = (15, 15))
    sns.swarmplot(x = "variables", y = "value", hue = "Outcome", data = diabetes_melted)
    plt.title("Swarmplot of all variavles by Outcome")
    plt.show()

#Gráfico de barras com a contagem de outcomes ou de GlycemiaValues
def outc_values(vcategorical):
    order = []
    if vcategorical=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    plt.figure()
    sns.countplot(x = diabetesdf[vcategorical], data = diabetesdf, hue_order=order)
    plt.title(f"Distribution of {vcategorical}")
    plt.show()

#outc_values("GlycemiaValues")

#grafico circular do outcome 0 e 1  e da variavel criada "GlycemiaValues"
def circular():
    labels= 'Not Diabetic','Diabetic'
    plt.figure(figsize=(10,7))
    plt.pie(diabetesdf['Outcome'].value_counts(),labels=labels,autopct='%0.02f%%')
    plt.legend()
    plt.show()
######Nota! Gráfico redundante porque já temos um barplot a dizer isto --> escolher qual usar

#separam o outcome 0 de 1
df_d0 = diabetes[diabetes['Outcome'] == 0]
df_d1 = diabetes[diabetes['Outcome'] == 1]

#and random sample the same amount of instances from the higher represented '0' class to match the available '1' class instances
df_d0_samp = df_d0.sample(268,replace = False)
df_bal = pd.concat([df_d1, df_d0_samp])

#histograma com função de densidade das variáveis em função do outcome
def histvout(): 
    cores = {0: 'blue', 1: 'green'}
    cores2 = {'Hypoglycemia': 'blue', 'Normal': 'green', 'Pre-diabetes': 'yellow'}
    variaveisnum= diabetes.columns[0:8]
    counter = 0
    for i in variaveisnum:
        counter += 1
        print(counter, ':', i)
        sns.displot(data = df_bal, kde=True, x = diabetes[str(i)], hue='Outcome', palette=cores)
        plt.title(f'"{i}" em função do Outcome')
    plt.plot()
    plt.show()

#Histogramas + boxplots (lado a lado) para uma variável numerica em função do outcome
def histpx():
    fig = px.histogram(diabetesdf, x = 'Glucose',
                    color = 'Outcome',
                    marginal = 'box',
                    barmode= 'overlay',
                    histnorm = 'density'
                    )

    fig.update_layout(
        title_font_color="black",
        legend_title_font_color="green",
        title={
            'text': "Glucose Histogram per Outcome",
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
    )
    fig.show()

#Problema: abre uma página no navegador e temos de ver se é dessa maneira que queremos visualizar o gráfico

# Pairplot
def pairplt():
    cores = {0: 'blue', 1: 'green'}
    plt.figure()
    sns.set(font_scale=0.7)
    sns.pairplot(diabetesdf, hue = "Outcome", diag_kind = "kde", palette = cores, plot_kws = {"s": 8})
    plt.title('Pairplot')
    plt.show()

#Matriz de correlações
def matrcorr():
    corr = diabetesdf.corr().round(2)
    plt.figure(figsize=(14, 10))
    sns.set(font_scale=1.15)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
    plt.title('Correlation Matrix')
    plt.show()

#função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def varscatter(variavel_1,variavel_2):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data=diabetesdf, x=variavel_1, y=variavel_2)
    plt.title(f"Scatterplot of {variavel_1} by {variavel_2}")
    plt.show()

#varscatter("Glucose","BMI")

#caso o utilizador opte por fazer em função ou do outcome ou da variavel "GlycemiaValues" incorporar esta função
def varscatter2(variavel1, variavel2, varcategorical):
    sns.scatterplot(data=diabetesdf, x=variavel1, y=variavel2, hue=varcategorical)
    plt.title(f"Scatterplot of {variavel1} by {variavel2} in order to {varcategorical}")
    plt.show()

#varscatter2("Glucose","BMI","Outcome")
#varscatter2("Glucose","BMI","GlycemiaValues")

#Nestas funções, as variáveis deviam ser pedidas pelo utlizador, ou seja input, 
#e depois eram feitas verificações caso o nome da variável não fosse correto