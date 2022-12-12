import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt

diabetes = pd.read_csv("diabetes.csv")

variaveis = diabetes.columns
diabetesdf=pd.DataFrame(data=diabetes, columns=diabetes.columns)
x=[]

print(diabetesdf)
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

diabetes.insert(loc=2, column="GlycemiaValues", value=x)
print(diabetes)

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc) e histograma para observar a distribuição4
colors = sns.color_palette('pastel')

print(diabetes.loc[2])

def varnum(variavel):
    print(variavel)
    print(diabetesdf[variavel].describe())
    sns.histplot(data=diabetesdf, x=variavel,kde=True)
    plt.title(f"Histogram of {variavel}")
    plt.show()
    sns.boxplot(data=diabetesdf, x=variavel)
    plt.title(f"Boxplot of {variavel}")
    plt.show()

varnum("Glucose")

#esta função permite ao utilizador escolher visualizar uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
def varhue(variavel, categoria):
    sns.histplot(data=diabetesdf, x=variavel, hue= categoria, legend=True)
    plt.show()

varhue("Glucose", "Outcome")
varhue("Glucose","GlycemiaValues")

def varboxplot (variavel,categoria):
    sns.boxplot(data=diabetesdf, x=variavel, y=categoria,hue=categoria)
    plt.show()

varboxplot("Glucose","Outcome")