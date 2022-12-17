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

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc) e histograma para observar a distribuição

def varnum(variavel):
    print(variavel)
    print(diabetesdf[variavel].describe())
    sns.histplot(data=diabetesdf, x=variavel,kde=True)
    plt.title(f"Histogram of {variavel}")
    plt.show()
    sns.boxplot(data=diabetesdf, x=variavel)
    plt.title(f"Boxplot of {variavel}")
    plt.show()

#varnum("Glucose")

#esta função permite ao utilizador escolher visualizar um histograma de uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
def varhue(variavel, categoria):
    sns.histplot(data=diabetesdf, x=variavel, hue= categoria, legend=True)
    plt.title(f"Histogram of {variavel} in order to {categoria}")
    plt.show()

#varhue("Glucose", "Outcome")
#varhue("Glucose","GlycemiaValues")

"""
#função para efetuar boxplots de uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
def varboxplot (variavel,categoria):
    sns.boxplot(data=diabetesdf, x=variavel, y=categoria,hue=categoria, dodge=False)
    plt.title(f"Boxplot of {variavel} by {categoria}")
    plt.show()

varboxplot("Glucose","Outcome")
"""

#função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def varscatter(variavel_1,variavel_2):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data=diabetesdf, x=variavel_1, y=variavel_2)
    plt.title(f"Scatterplot of {variavel_2} by {variavel_1}")
    plt.show()

#varscatter("Glucose","BMI")
#varscatter("DiabetesPedigreeFunction","Outcome")

#caso o utilizador opte por fazer em função ou do outcome ou da variavel "GlycemiaValues" incorporar esta função
def varscatter2(variavel1, variavel2, varcategorical):
    sns.scatterplot(data=diabetesdf, x=variavel1, y=variavel2, hue=varcategorical)
    plt.title(f"Scatterplot of {variavel2} by {variavel1} in order to {varcategorical}")
    plt.show()

#varscatter2("Glucose","BMI","Outcome")
#varscatter2("Glucose","BMI","GlycemiaValues")

#matriz de graficos de dispersão que inclui todas as variaveis - tenho de melhorar
def scattermat (vcategorical):
    sns.set_theme(style="ticks")
    order = []
    if vcategorical=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    sns.pairplot(diabetesdf, hue= vcategorical, hue_order=order)
    plt.title(f"Scatterplot Matrix by {vcategorical}")
    plt.show()

# scattermat("GlycemiaValues")
#scattermat("Outcome")

#histograma e função densididade para cada uma das variaveis em função do "Outcome" e "GlycemiaValues" => tentar alterar pallete
def variaveiscat(variavel , categoria):
    if categoria=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    sns.histplot(data=diabetesdf, x=variavel,kde=True, hue=categoria, hue_order=order)
    plt.title(f"Histogram of {variavel} by {categoria}")
    plt.show()

#variaveiscat("Age","Outcome")
#variaveiscat("Insulin","GlycemiaValues")

#histograma e função densididade de TODAS as variaveis em função do "Outcome" e "GlycemiaValues"
def hist_total():
    counter = 0
    for i in variaveis:
        counter += 1
        print(counter, ':', i)
        plt.subplot(3, 3, counter)
        sns.histplot(data = diabetesdf, x = diabetesdf[str(i)], hue = "Outcome", multiple  = 'dodge', kde=True)
    plt.suptitle("Histogram of all variables by Outcome", fontsize=16)
    plt.plot()
    plt.show()


df_d0 = diabetesdf[diabetesdf['Outcome'] == 0]
df_d1 = diabetesdf[diabetesdf['Outcome'] == 1]

#and random sample the same amount of instances from the higher represented '0' class to match the available '1' class instances
df_d0_samp = df_d0.sample(264,replace = False) # this time 264 is the sample number for reason as we see above
df_bal = pd.concat([df_d1, df_d0_samp]) #putting back the two class together

def regressao (variavel1,variavel2):
    sns.regplot(x=variavel1, y=variavel2, data=df_bal[df_bal['Outcome'] == 0], color='blue')
    sns.regplot(x=variavel1, y=variavel2, data=df_bal[df_bal['Outcome'] == 1], color='green')
    plt.title(f"{variavel1} vs {variavel2} scatterplot")
    plt.show()

#regressao("Glucose","Age")

def catplotvar(variavel):
    sns.catplot(x = "Outcome", y = variavel, hue = "Outcome", kind = "swarm", data = diabetesdf)
    plt.title(f"Swarmplot of {variavel}")
    plt.show()

#catplotvar("BMI")

#tabela da dataframe - 1 ou tabela com propriedades estatísticas das variáveis numéricas -2
def tabelas(dataframe, id):
    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    if id==1:
        tabela= ax.table(cellText=dataframe.values[0:25], colWidths = [0.1]*len(dataframe.columns),  colLabels=dataframe.columns, loc='center')
    else:
        desc=dataframe.describe()
        rownames= desc.axes[0].tolist()
        tabela= ax.table(cellText=desc.values, colWidths = [0.1]*len(dataframe.columns),  colLabels=dataframe.columns, rowLabels= rownames, loc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)
    plt.show()

#tabelas(diabetesdf, 1)
#tabelas(diabetesdf,2)

def boxplot_total():
    sns.boxplot(data=diabetesdf)
    plt.title(f"Boxplot of the all variables")
    plt.show()

#boxplot_total()