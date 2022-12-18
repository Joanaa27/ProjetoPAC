#Importação de pacotes
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Leitura de base de dados
diabetes = pd.read_csv("diabetes.csv")
diabetesdf = pd.DataFrame(diabetes)
#variaveis = diabetes.columns

#tabela da dataframe - 1 ou tabela com propriedades estatísticas das variáveis numéricas -2
def tabelas(dataframe, id):
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    if id == 1:
        tabela = ax.table(cellText = dataframe.values[0:25].round(2), colWidths = [0.1] * len(dataframe.columns), colLabels = dataframe.columns, loc = 'center')
        
    else:
        desc = dataframe.describe()
        print(desc.values)
        rownames = desc.axes[0].tolist()
        tabela = ax.table(cellText = desc.values.round(2), colWidths = [0.1] * len(dataframe.columns), colLabels = dataframe.columns, rowLabels = rownames, loc = 'center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    plt.show()

#tabelas(diabetesdf, 1)
#tabelas(diabetesdf, 2)

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc), histograma e boxplot para observar a distribuição 
def var_num(dataframe, variaveis):
    for i in variaveis:
        fig, ax = plt.subplots()
        ax.axis('off')
        ax.axis('tight')
        df_var = dataframe[i].describe()
        colnames = df_var.axes[0].tolist()
        tabela = ax.table(cellText = [df_var.values.round(2)],colLabels=colnames, loc = 'center')
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(8)
        plt.title(f"Table of statistical values of {i}")
        plt.show()
    
        sns.histplot(data = dataframe, x=i)
        plt.title(f"Histogram of {i}")
        plt.show()

        sns.boxplot(data = dataframe, x = i)
        plt.title(f"Boxplot of {i}")
        plt.show()

#var_num(diabetesdf,["Insulin"])

#histograma e função densididade de TODAS as variaveis em função do "Outcome" e "GlycemiaValues"
def hist_total(dataframe,has_outcome = False):
    variaveis = dataframe.columns
    counter = 0
    for i in variaveis:
        counter += 1
        print(counter, ':', i)
        plt.subplot(3, 3, counter)
        sns.histplot(data = dataframe, x = dataframe[str(i)], hue = "Outcome", multiple  = 'dodge', kde = True) if has_outcome else sns.histplot(data = dataframe, x = dataframe[str(i)], multiple  = 'dodge', kde = True)
    plt.suptitle("Histogram of all variables by Outcome", fontsize = 16) if has_outcome else plt.suptitle("Histogram of all variables", fontsize = 16)
    plt.plot()
    plt.show()

#hist_total(diabetesdf)
#hist_total(diabetesdf, True)

def regressao (dataframe, variavel_1, variavel_2, vcategorical = None):
    if vcategorical == "Outcome":
        #separam o outcome 0 de 1
        df_d0 = dataframe[dataframe['Outcome'] == 0]
        df_d1 = dataframe[dataframe['Outcome'] == 1]
        #executamos uma amostra aleatoria com o mesmo numero de observações da categoria mais representada, 
        #neste caso 0 para dar "match" com as observações da categoria 1
        df_d0_samp = df_d0.sample(268,replace = False)
        df_bal = pd.concat([df_d1, df_d0_samp])
        sns.regplot(x = variavel_1, y = variavel_2, data = df_bal[df_bal['Outcome'] == 0], color = 'blue')
        sns.regplot(x = variavel_1, y = variavel_2, data = df_bal[df_bal['Outcome'] == 1], color = 'green')

    elif vcategorical=="GlycemiaValues":
        df_d0 = dataframe[dataframe['GlycemiaValues'] == "Hypoglycemia"]
        df_d1 = dataframe[dataframe['GlycemiaValues'] == "Normal"]
        df_d2 = dataframe[dataframe['GlycemiaValues'] == "Pre-diabetes"]
        df_d1_samp = df_d1.sample(560,replace = False)
        df_bal = pd.concat([df_d0,df_d2, df_d1_samp])
        sns.regplot(x = variavel_1, y = variavel_2, data = df_bal[df_bal['GlycemiaValues'] == "Hypoglycemia"], color = 'yellow')
        sns.regplot(x = variavel_1, y = variavel_2, data = df_bal[df_bal['GlycemiaValues'] == "Normal"], color = 'green')
        sns.regplot(x = variavel_1, y = variavel_2, data = df_bal[df_bal['GlycemiaValues'] == "Pre-diabetes"], color = 'blue')

    else:
        sns.regplot(x = variavel_1, y = variavel_2, data = dataframe, color = 'blue')

    plt.title(f"{variavel_1} vs {variavel_2} scatterplot by {vcategorical}")
    plt.show()

#regressao(diabetesdf, "Glucose", "Age", "GlycemiaValues")
#regressao(diabetesdf, "Glucose", "Age", "Outcome")
#regressao(diabetesdf, "Glucose", "Age")

def swarmplotvar(dataframe, variaveis, vcategorical = None):
    for s in variaveis:
        sns.catplot(x = vcategorical, y = s, hue = vcategorical, kind = "swarm", data = dataframe) 
        plt.title(f"Swarmplot of {s} by {vcategorical}")
        plt.show()

#swarmplotvar(diabetesdf,["BMI"],"Outcome")
#swarmplotvar(diabetesdf,"BMI","GlycemiaValues")
#swarmplotvar(diabetesdf,"BMI")

#boxplot de todas as variáveis em função da variavel "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na dataframe
#dropvalues - é uma lista com as variaveis que o utilizador nao quer vizualizar, sendo que a variavel "GlycemiaValues é obrigatória de descartar
def boxplot_all(dataframe, drop_values, has_outcome = False):
    diabetesbp = dataframe.drop(drop_values, axis = 1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")
    
    plt.figure(figsize = (15, 15))

    sns.boxplot(data = diabetes_melted, x = "variables", y = "value", hue = "Outcome") if has_outcome else sns.boxplot(data = diabetes_melted, x = "variables", y = "value")
    plt.title("Boxplot of numeric variables by Outcome") if has_outcome else plt.title("Boxplot of numeric variables")
    plt.show()

#boxplot_all(diabetesdf, ["BMI","Insulin"], True)

#stripplot de todas as variavem em função da variável "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na dataframe0
def stripvar(dataframe, drop_values, has_outcome = False):
    diabetesbp= dataframe.drop(drop_values, axis = 1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")
    
    plt.figure(figsize = (15, 15))
    sns.stripplot(x = "variables", y = "value", hue = "Outcome", data = diabetes_melted) if has_outcome else sns.stripplot(x = "variables", y = "value", data = diabetes_melted)
    plt.title("Stripplot of numeric variables by Outcome")  if has_outcome else plt.title("Stripplot of numeric variables")
    plt.show()

#stripvar(diabetesdf,["GlycemiaValues","Insulin"],True)

#Gráfico de barras com a contagem de outcomes ou de GlycemiaValues
def categorica_values(dataframe, vcategorical):
    order = []
    if vcategorical == "Outcome":
        order = [0,1]
    else:
        order = ['Hypoglycemia','Normal','Pre-diabetes']
    plt.figure()
    sns.countplot(x = dataframe[vcategorical], data = dataframe, hue_order = order)
    plt.title(f"Distribution of {vcategorical}")
    plt.show()

#categorica_values("GlycemiaValues")

#grafico circular do outcome 0 e 1  e da variavel criada "GlycemiaValues"
def circular(dataframe, vcategorical):
    labels = []
    if vcategorical == "Outcome":
        labels = {'Not Diabetic', 'Diabetic'}
    else:
        labels = {'Normal':'Normal','Pre-diabetes':'Pre-diabetes','Hypoglycemia':'Hypoglycemia'}

    plt.figure(figsize = (10,7))
    plt.pie(dataframe[vcategorical].value_counts(), labels = labels, autopct = '%0.02f%%')
    plt.legend()
    plt.show()

#print((diabetesdf["GlycemiaValues"] == "Normal").value_counts()) #560
#circular(diabetesdf, "Outcome")

def hist_vcat(dataframe, vcategorical, variaveis): 

    if vcategorical == "Outcome":
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
        df_d1_samp = df_d1.sample(560, replace = False)
        df_bal = pd.concat([df_d0,df_d2, df_d1_samp])
        cores = {'Hypoglycemia': 'yellow', 'Normal': 'green', 'Pre-diabetes': 'blue'}

    counter = 0
    for var in variaveis:
        counter += 1
        print(counter, ':', var)
        sns.displot(data = df_bal, kde=True, x = dataframe[str(var)], hue=vcategorical, palette=cores)
        plt.title(f'"{var}" by {vcategorical}')
    plt.plot()
    plt.show()

#hist_vcat(diabetesdf,"GlycemiaValues",["Glucose"])

# Pairplot
def pairplt(dataframe, vcategorical = None):
    if vcategorical == "Outcome":
        cores = {0: 'blue', 1: 'green'}
    elif vcategorical == "GlycemiaValues":
        cores = {'Hypoglycemia': 'yellow', 'Normal': 'green', 'Pre-diabetes': 'blue'}
    else:
        cores = None

    plt.figure()
    sns.set(font_scale = 0.7)
    sns.pairplot(dataframe, hue = vcategorical, diag_kind = "kde", palette = cores, plot_kws = {"s": 8})
    plt.title(f"Pairplot of all numeric variables by {vcategorical}")
    plt.show()

#pairplt(diabetesdf, "GlycemiaValues")
#pairplt(diabetesdf)

#Matriz de correlações
def matrcorr(dataframe):
    corr = dataframe.corr().round(2)
    plt.figure(figsize = (14, 10))
    sns.set(font_scale = 1.15)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
    plt.title('Correlation Matrix')
    plt.show()

#matrcorr(diabetesdf)

#função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def scatterplt(dataframe, variavel_1, variavel_2, vcategorical = None):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data = dataframe, x = variavel_1, y = variavel_2, hue = vcategorical)
    plt.title(f"Scatterplot of {variavel_1} by {variavel_2} in order to {vcategorical}") if vcategorical is not None else plt.title(f"Scatterplot of {variavel_1} by {variavel_2}") 
    plt.show()

#scatterplt(diabetesdf,"Glucose","BMI")
#scatterplt(diabetesdf,"Glucose","BMI","GlycemiaValues")


#######################################################################################
#Histogramas + boxplots (lado a lado) para uma variável numerica em função do outcome
def histpx(dataframe):
    fig = px.histogram(dataframe, x = 'Glucose',
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
    #fig.show()
#Problema: abre uma página no navegador e temos de ver se é dessa maneira que queremos visualizar o gráfico
