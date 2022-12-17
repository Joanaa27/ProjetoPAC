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

#boxplot de todas as variáveis em função da variavel "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na dataframe
#dropvalues - é uma lista com as variaveis que o utilizador nao quer vizualizar, sendo que a variavel "GlycemiaValues é obrigatória de descartar
def boxplot_all(dataframe,drop_values, has_outcome=False):
   
    diabetesbp= dataframe.drop(drop_values, axis=1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")
    
    plt.figure(figsize = (15, 15))

    sns.boxplot(data = diabetes_melted, x="variables", y="value", hue="Outcome") if has_outcome else sns.boxplot(data = diabetes_melted, x="variables", y="value")
    plt.title("Boxplot of numeric variables by Outcome") if has_outcome else plt.title("Boxplot of numeric variables")
    plt.show()

#boxplot_all(diabetesdf)


#stripplot de todas as variavem em função da variável "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na dataframe0
def stripvar(dataframe, drop_values, has_outcome=False):
    diabetesbp= dataframe.drop(drop_values, axis=1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")
    
    plt.figure(figsize = (15, 15))
    sns.stripplot(x = "variables", y = "value", hue = "Outcome", data = diabetes_melted) if has_outcome else sns.stripplot(x = "variables", y = "value", data = diabetes_melted)
    plt.title("Stripplot of numeric variables by Outcome")  if has_outcome else plt.title("Stripplot of numeric variables")
    plt.show()

stripvar(diabetesdf,["GlycemiaValues","Insulin"],True)

#Gráfico de barras com a contagem de outcomes ou de GlycemiaValues
def outc_values(dataframe, vcategorical):
    order = []
    if vcategorical=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    plt.figure()
    sns.countplot(x = dataframe[vcategorical], data = dataframe, hue_order=order)
    plt.title(f"Distribution of {vcategorical}")
    plt.show()

#outc_values("GlycemiaValues")

#grafico circular do outcome 0 e 1  e da variavel criada "GlycemiaValues"
def circular(dataframe, vcategorical):
    labels=[]
    if vcategorical=="Outcome":
        labels= {'Not Diabetic', 'Diabetic'}
    else:
        labels={'Normal':'Normal','Pre-diabetes':'Pre-diabetes','Hypoglycemia':'Hypoglycemia'}

    plt.figure(figsize=(10,7))
    plt.pie(dataframe[vcategorical].value_counts(),labels=labels,autopct='%0.02f%%')
    plt.legend()
    plt.show()

#print((diabetesdf["GlycemiaValues"]=="Normal").value_counts()) #560
#circular(diabetesdf,"Outcome")

#histograma com função de densidade das variáveis em função do outcome ou glycemiavalues
def hist_vcat(dataframe, vcategorical): 

    if vcategorical=="Outcome":
        #separam o outcome 0 de 1
        df_d0 = dataframe[dataframe['Outcome'] == 0]
        df_d1 = dataframe[dataframe['Outcome'] == 1]
        #executamos uma amostra aleatoria com o mesmo numero de observações da categoria mais representada, 
        #neste caso 0 para dar "match" com as observações da categoria 1
        df_d0_samp = df_d0.sample(268,replace = False)
        df_bal = pd.concat([df_d1, df_d0_samp])
        cores = {0: 'blue', 1: 'green'}
    else:
        df_d0 = dataframe[dataframe['GlycemiaValues'] == "Hypoglycemia"]
        df_d1 = dataframe[dataframe['GlycemiaValues'] == "Normal"]
        df_d2 = dataframe[dataframe['GlycemiaValues'] == "Pre-diabetes"]
        df_d1_samp = df_d1.sample(560,replace = False)
        df_bal = pd.concat([df_d0,df_d2, df_d1_samp])
        cores = {'Hypoglycemia': 'yellow', 'Normal': 'green', 'Pre-diabetes': 'blue'}


    variaveis= diabetes.columns #usamos diabetes, porque nao queremos a variavel que criamos
    counter = 0
    for val in variaveis:
        counter += 1
        print(counter, ':', val)
        sns.displot(data = df_bal, kde=True, x = diabetes[str(val)], hue=vcategorical, palette=cores)
        plt.title(f'"{val}" by {vcategorical}')
    plt.plot()
    plt.show()

#hist_vcat(diabetesdf,"GlycemiaValues")

# Pairplot
def pairplt(dataframe,vcategorical=None):
    if vcategorical=="Outcome":
        cores = {0: 'blue', 1: 'green'}
    elif vcategorical=="GlycemiaValues":
        cores = {'Hypoglycemia': 'yellow', 'Normal': 'green', 'Pre-diabetes': 'blue'}
    else:
        cores = None

    plt.figure()
    sns.set(font_scale=0.7)
    sns.pairplot(dataframe, hue = vcategorical, diag_kind = "kde", palette = cores, plot_kws = {"s": 8})
    plt.title(f"Pairplot of all numeric variables by {vcategorical}")
    plt.show()

#pairplt(diabetesdf,"GlycemiaValues")
#pairplt(diabetesdf)

#Matriz de correlações
def matrcorr(dataframe):
    corr = dataframe.corr().round(2)
    plt.figure(figsize=(14, 10))
    sns.set(font_scale=1.15)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
    plt.title('Correlation Matrix')
    plt.show()

#matrcorr(diabetesdf)

#função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def scatterplt(dataframe,variavel_1,variavel_2, vcategorical=None):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data=dataframe, x=variavel_1, y=variavel_2, hue=vcategorical)
    plt.title(f"Scatterplot of {variavel_1} by {variavel_2} in order to {vcategorical}") if vcategorical is not None else plt.title(f"Scatterplot of {variavel_1} by {variavel_2}") 
    plt.show()

#scatterplt(diabetesdf,"Glucose","BMI")
#scatterplt(diabetesdf,"Glucose","BMI","GlycemiaValues")

#######################################################################################
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