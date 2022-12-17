import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px

diabetes = pd.read_csv("diabetes.csv")

variaveis = diabetes.columns
diabetesdf=pd.DataFrame(data=diabetes, columns=diabetes.columns)
x=[]
print(diabetesdf)
for i in diabetesdf["Glucose"]:
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

diabetesdf.insert(loc=2, column="GlycemiaValues", value=x)
#print(diabetesdf.loc[2])

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc), histograma e boxplot para observar a distribuição 
def var_num(dataframe, variavel):
    print(variavel)
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    df_var=dataframe[variavel].describe()
    colnames= df_var.axes[0].tolist()
    tabela= ax.table(cellText=[df_var.values.round(2)],colLabels=colnames, loc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    print(f"Tabela das medidas estatísticas de {variavel}")
    plt.show()
    
    sns.histplot(data=dataframe, x=variavel,kde=True)
    plt.title(f"Histogram of {variavel}")
    plt.show()

    sns.boxplot(data=dataframe, x=variavel)
    plt.title(f"Boxplot of {variavel}")
    plt.show()

#var_num(diabetesdf,"Insulin")

"""
#função para efetuar boxplots de uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
def varboxplot (variavel,categoria):
    sns.boxplot(data=diabetesdf, x=variavel, y=categoria,hue=categoria, dodge=False)
    plt.title(f"Boxplot of {variavel} by {categoria}")
    plt.show()

varboxplot("Glucose","Outcome")
"""

#histograma e função densididade de TODAS as variaveis em função do "Outcome" e "GlycemiaValues"
def hist_total(dataframe,has_outcome=False):
    counter = 0
    for i in variaveis:
        counter += 1
        print(counter, ':', i)
        plt.subplot(3, 3, counter)
        sns.histplot(data = dataframe, x = dataframe[str(i)], hue = "Outcome", multiple  = 'dodge', kde=True) if has_outcome else sns.histplot(data = dataframe, x = dataframe[str(i)], multiple  = 'dodge', kde=True)
    plt.suptitle("Histogram of all variables by Outcome", fontsize=16) if has_outcome else plt.suptitle("Histogram of all variables", fontsize=16)
    plt.plot()
    plt.show()

#hist_total(diabetesdf)
#hist_total(diabetesdf,True)

def regressao (dataframe,variavel_1,variavel_2,vcategorical=None):
    if vcategorical=="Outcome":
        #separam o outcome 0 de 1
        df_d0 = dataframe[dataframe['Outcome'] == 0]
        df_d1 = dataframe[dataframe['Outcome'] == 1]
        #executamos uma amostra aleatoria com o mesmo numero de observações da categoria mais representada, 
        #neste caso 0 para dar "match" com as observações da categoria 1
        df_d0_samp = df_d0.sample(268,replace = False)
        df_bal = pd.concat([df_d1, df_d0_samp])
        sns.regplot(x=variavel_1, y=variavel_2, data=df_bal[df_bal['Outcome'] == 0], color='blue')
        sns.regplot(x=variavel_1, y=variavel_2, data=df_bal[df_bal['Outcome'] == 1], color='green')

    elif vcategorical=="GlycemiaValues":
        df_d0 = dataframe[dataframe['GlycemiaValues'] == "Hypoglycemia"]
        df_d1 = dataframe[dataframe['GlycemiaValues'] == "Normal"]
        df_d2 = dataframe[dataframe['GlycemiaValues'] == "Pre-diabetes"]
        df_d1_samp = df_d1.sample(560,replace = False)
        df_bal = pd.concat([df_d0,df_d2, df_d1_samp])
        sns.regplot(x=variavel_1, y=variavel_2, data=df_bal[df_bal['GlycemiaValues'] == "Hypoglycemia"], color='yellow')
        sns.regplot(x=variavel_1, y=variavel_2, data=df_bal[df_bal['GlycemiaValues'] == "Normal"], color='green')
        sns.regplot(x=variavel_1, y=variavel_2, data=df_bal[df_bal['GlycemiaValues'] == "Pre-diabetes"], color='blue')

    else:
        sns.regplot(x=variavel_1, y=variavel_2, data=dataframe, color='blue')

    plt.title(f"{variavel_1} vs {variavel_2} scatterplot by {vcategorical}")
    plt.show()

#regressao(diabetesdf,"Glucose","Age","GlycemiaValues")
#regressao(diabetesdf,"Glucose","Age","Outcome")
#regressao(diabetesdf,"Glucose","Age")

def catplotvar(dataframe,variavel,vcategorical=None):
    sns.catplot(x = vcategorical, y = variavel, hue = vcategorical, kind = "swarm", data = dataframe) 
    plt.title(f"Swarmplot of {variavel} by {vcategorical}")
    plt.show()

#catplotvar(diabetesdf,"BMI","Outcome")
#catplotvar(diabetesdf,"BMI","GlycemiaValues")
#catplotvar(diabetesdf,"BMI")

#tabela da dataframe - 1 ou tabela com propriedades estatísticas das variáveis numéricas -2
def tabelas(dataframe, id):
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    if id==1:
        tabela= ax.table(cellText=dataframe.values[0:25], colWidths = [0.1]*len(dataframe.columns),  colLabels=dataframe.columns, loc='center')
    else:
        desc=dataframe.describe()
        print(desc.values)
        rownames= desc.axes[0].tolist()
        tabela= ax.table(cellText=desc.values, colWidths = [0.1]*len(dataframe.columns),  colLabels=dataframe.columns, rowLabels= rownames, loc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    plt.show()

#tabelas(diabetesdf, 1)
#tabelas(diabetesdf,2)