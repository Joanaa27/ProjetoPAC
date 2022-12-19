#Importação de pacotes
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#NOTA: todos os gráficos definidos em funções neste documento incluem uma linha de código que permite que o(s) gráfico(s) e tabela(s) que foram chamados
#e visualizados (ou seja, escolhidos pelo utilizador) no ficheiro main.py sejam automaticamente guardados em ficheiro .png

### FUNÇÕES ###

#tabela da dataframe (1) ou tabela com propriedades estatísticas das variáveis numéricas (2)
#o parametro id permite identificar e escolher entre fazer uma tabela com as primeiras 25 observações ou uma tabela com medidas estatisticas 
#de todas as variaveis, respetivamente
def tabelas(dataframe, id):
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    if id == 1:
        tabela = ax.table(cellText = dataframe.values[0:25], colWidths = [0.1] * len(dataframe.columns), colLabels = dataframe.columns, loc = 'center')
        
    else:
        desc = dataframe.describe()
        rownames = desc.axes[0].tolist()
        tabela = ax.table(cellText = desc.values.round(2), colWidths = [0.1] * len(dataframe.columns), colLabels = dataframe.columns, rowLabels = rownames, loc = 'center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    plt.savefig("tabela.png")
    plt.show()

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc), histograma e boxplot para observar a distribuição da variavel em questao
#parametro variaveis - permite escolher 1 ou mais variaveis 
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
        plt.savefig("tabela_stats.png")
        plt.show()
    
        sns.histplot(data = dataframe, x=i)
        plt.title(f"Histogram of {i}")
        plt.savefig("histogram_variavel_numerica.png")
        plt.show()

        sns.boxplot(data = dataframe, x = i)
        plt.title(f"Boxplot of {i}")
        plt.savefig("boxplot_variavel_numerica.png")
        plt.show()

#histograma e função densididade de todas as variaveis em função do "Outcome" ou não, de forma conjunta
#parametro has_outcome, permite escolher fazer ou não o gráfico em função do outcome
def hist_total(dataframe, has_outcome = False):
    variaveis = dataframe.columns
    counter = 1
    for i in variaveis:
        
        print(counter, ':', i)
        plt.subplot(2,5,counter)
        sns.histplot(data = dataframe, x = dataframe[str(i)], hue = "Outcome", multiple  = 'dodge', kde = True) if has_outcome else sns.histplot(data = dataframe, x = dataframe[str(i)], multiple  = 'dodge', kde = True)
        counter += 1
    
    plt.suptitle("Histogram of all variables by Outcome", fontsize = 16) if has_outcome else plt.suptitle("Histogram of all variables", fontsize = 16)
    plt.plot()
    plt.savefig("histogram_all.png")
    plt.show()

#gráfico de dispersão com a reta de regressão linear
#parametro variavel_1 - permite escolher a primeira variavel do eixo dos xx
#parametro variavel_2 - permite escolher a primeira variavel do eixo dos yy
#vcategorical - permite fazer este grafico em função de uma das 2 variaveis categoricas ("Outcome" e "GlycemiaValues") ou de nenhuma destas,
#ou seja, sem qualquer dependência
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
    plt.savefig("regressao.png")
    plt.show()

#swarmplot das variaveis numericas de forma individual
#parametro variaveis - permite escolher 1 ou mais variaveis
#parametro vcategorical - permite fazer este grafico em função de uma das 2 variaveis categoricas ("Outcome" e "GlycemiaValues") ou de nenhuma destas,
#ou seja, sem qualquer dependência
def swarmplotvar(dataframe, variaveis, vcategorical = None):
    for s in variaveis:
        sns.catplot(x = vcategorical, y = s, hue = vcategorical, kind = "swarm", data = dataframe) 
        plt.title(f"Swarmplot of {s} by {vcategorical}")
        plt.savefig("swarmplot.png")
        plt.show()

#boxplot de todas as variáveis em função da variavel "Outcome" ou não, apresentadas de forma conjunta
#parametro dropvalues - é uma lista com as variaveis que o utilizador nao quer vizualizar, 
#sendo que a variavel "GlycemiaValues é obrigatória de descartar, daí estar já incluida no codigo
#parametro has_outcome, permite escolher fazer ou não o gráfico em função do outcome
def boxplot_all(dataframe, drop_values, has_outcome = False):
    diabetesbp = dataframe.drop(drop_values, axis = 1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")
    
    plt.figure(figsize = (15, 15))

    sns.boxplot(data = diabetes_melted, x = "variables", y = "value", hue = "Outcome") if has_outcome else sns.boxplot(data = diabetes_melted, x = "variables", y = "value")
    plt.title("Boxplot of numeric variables by Outcome") if has_outcome else plt.title("Boxplot of numeric variables")
    plt.savefig("boxplot_all.png")
    plt.show()

#stripplot de todas as variaveis numericas em função da variável "Outcome" ou não (parametro has_outcome)
#mais uma vez eliminamos a coluna GlycemiaValues porque não queremos e não faz sentido esta aparecer nesta analise
#parametros iguais à função de cima
def stripvar(dataframe, drop_values, has_outcome = False):
    diabetesbp = dataframe.drop(drop_values, axis = 1)
    diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")

    plt.figure(figsize = (15, 15))
    sns.stripplot(x = "variables", y = "value", hue = "Outcome", data = diabetes_melted) if has_outcome else sns.stripplot(x = "variables", y = "value", data = diabetes_melted)
    plt.title("Stripplot of numeric variables by Outcome")  if has_outcome else plt.title("Stripplot of numeric variables")
    plt.savefig("stripplot.png")
    plt.show()

#Gráfico de barras com a contagem de outcomes ou de GlycemiaValues (variaveis categoricas - vcategorical)
def categorica_values(dataframe, vcategorical):
    order = []
    if vcategorical == "Outcome":
        order = [0,1]
    else:
        order = ['Hypoglycemia','Normal','Pre-diabetes']
    plt.figure()
    sns.countplot(x = dataframe[vcategorical], data = dataframe, hue_order = order)
    plt.title(f"Distribution of {vcategorical}")
    plt.savefig("barplot_variavel_categorica.png")
    plt.show()

#grafico circular do outcome  e da variavel criada "GlycemiaValues" (vcategorical), definido em percentagem 
def circular(dataframe, vcategorical):
    labels = []
    if vcategorical == "Outcome":
        labels = {'Diabetic', 'Not Diabetic'}
    else:
        labels = {'Normal':'Normal','Pre-diabetes':'Pre-diabetes','Hypoglycemia':'Hypoglycemia'}

    plt.figure(figsize = (10,7))
    plt.pie(dataframe[vcategorical].value_counts(), labels = labels, autopct = '%0.02f%%')
    plt.legend()
    plt.savefig("circular_var_categorica.png")
    plt.show()

#histograma com função densidade para as variaveis numericas 1 ou mais (parametro - variaveis) em função do Outcome ou da variavel GlycemiaValues (vcategorical)
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
        plt.title(f'Histogram of "{var}" by {vcategorical}')
    plt.plot()
    plt.savefig("histogram_variaveis_numericas.png")
    plt.show()

#Pairplot - inclui graficos de dispersao e de densidade entre todas as variaveis(correlograma)
#parametro vcategorical - permite fazer este grafico em função de uma das 2 variaveis categoricas ("Outcome" e "GlycemiaValues") ou de nenhuma destas,
#ou seja, sem qualquer dependência
def pairplt(dataframe, vcategorical = None):
    plt.figure()
    sns.set(font_scale = 0.7)
    sns.pairplot(dataframe, hue = vcategorical, diag_kind = "kde", plot_kws = {"s": 8})
    plt.title(f"Pairplot of all numeric variables by {vcategorical}")
    plt.savefig("pairplot.png")
    plt.show()

#Matriz de correlações - apresenta as correlações e a respetiva força (atraves do coeficiente de correlação mostrado) entre as variaveis 
def matrcorr(dataframe):
    corr = dataframe.corr().round(2)
    plt.figure(figsize = (14, 10))
    sns.set(font_scale = 1.15)
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
    plt.title('Correlation Matrix')
    plt.savefig("correlation_matrix.png")
    plt.show()

#função que executa gráficos de dispersão entre as variaveis numericas escolhidas pelo utilizador
#parametro variavel_1 - permite escolher a primeira variavel do eixo dos xx
#parametro variavel_2 - permite escolher a primeira variavel do eixo dos yy
#vcategorical - permite fazer este grafico em função de uma das 2 variaveis categoricas ("Outcome" e "GlycemiaValues") ou de nenhuma destas,
#ou seja, sem qualquer dependência
def scatterplt(dataframe, variavel_1, variavel_2, vcategorical = None):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data = dataframe, x = variavel_1, y = variavel_2, hue = vcategorical)
    plt.title(f"Scatterplot of {variavel_1} by {variavel_2} in order to {vcategorical}") if vcategorical is not None else plt.title(f"Scatterplot of {variavel_1} by {variavel_2}") 
    plt.savefig("scatterplot.png")
    plt.show()