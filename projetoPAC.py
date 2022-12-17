import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly_express as px

print("Projeto de PAC - Base de dados 'Diabetes'")

#ler o ficheiro csv
diabetes = pd.read_csv("diabetes.csv")

#transformar em dataframe
diabetesdf=pd.DataFrame(diabetes)
#print(diabetesdf)
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
#diabetesdf.info()