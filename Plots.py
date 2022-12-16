#Importação de pacotes
import missingno as msno
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

#Leitura de base de dados
diabetes = pd.read_csv("diabetes.csv")
variaveis = diabetes.columns[:8]
diabetesdf=pd.DataFrame(data=diabetes, columns=diabetes.columns)

'''
#Checking missing values and data types
msno.matrix(diabetesdf)
plt.show()
'''

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
print(diabetes)

#Gráfico de barras com a contagem de outcomes
plt.figure()
sns.countplot(x = diabetesdf["Outcome"], data = diabetesdf, saturation = 1)
plt.title("Distribution of Outcome Values")
plt.show()

#Gráfico de barras para a GlycemiaValues
sns.set(style="darkgrid")
ax = sns.countplot(x="GlycemiaValues", data=diabetesdf, order=['Hypoglycemia','Normal','Pre-diabetes'])
plt.title('Gráfico de barras para a variável categoria GlycemiaValues')
plt.show()

#grafico circular do outcome 0 e 1  e da variavel criada "GlycemiaValues"
colors = sns.color_palette('pastel')
labels= 'Not Diabetic','Diabetic'
plt.figure(figsize=(10,7))
plt.pie(diabetes['Outcome'].value_counts(),labels=labels,colors=colors,autopct='%0.02f%%')
plt.legend()
plt.show()
######Nota! Gráfico redundante porque já temos um barplot a dizer isto --> escolher qual usar

#Histogramas + boxplots (lado a lado) para uma variável numerica em função do outcome
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
cores = {0: 'blue', 1: 'green'}
plt.figure()
sns.set(font_scale=0.7, style="darkgrid")
sns.pairplot(diabetesdf, hue = "Outcome", diag_kind = "kde", palette = cores, plot_kws = {"s": 8})
plt.title('Pairplot')
plt.show()

#Matriz de correlações
corr = diabetesdf.corr().round(2)
plt.figure(figsize=(14, 10))
sns.set(font_scale=1.15)
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
plt.title('Correlation Matrix')
plt.show()