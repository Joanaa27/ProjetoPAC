#Importação de pacotes
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

#separam o outcome 0 de 1
df_d0 = diabetes[diabetes['Outcome'] == 0]
df_d1 = diabetes[diabetes['Outcome'] == 1]

#and random sample the same amount of instances from the higher represented '0' class to match the available '1' class instances
df_d0_samp = df_d0.sample(268,replace = False)
df_bal = pd.concat([df_d1, df_d0_samp])

plt.figure()
sns.countplot(x = diabetesdf["Outcome"], data = diabetesdf, saturation = 1)
plt.title("Distribution of Outcome Values")
plt.show()

'''
#histograma com função de densidade das variáveis em função do outcome
cores = {0: 'blue', 1: 'green'}
counter = 0
for i in variaveis:
    counter += 1
    print(counter, ':', i)
    sns.displot(data = df_bal, kde=True, x = diabetes[str(i)], hue='Outcome', palette=cores)
    plt.title(f'"{i}" em função do Outcome')
plt.plot()
plt.show()

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
'''

#Matriz de correlações
corr=diabetesdf.corr().round(2)

sns.set(font_scale=1.15)
plt.figure(figsize=(14, 10))
#sns.color_palette('pastel')
sns.set_palette('pastel')
sns.set_style('white')
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr,annot=True,cmap='gist_yarg_r',mask=mask,cbar=True)
plt.title('Correlation Plot')
plt.show()

'''
#grafico circular do outcome 0 e 1  e da variavel criada "GlycemiaValues"
colors = sns.color_palette('pastel')
labels= 'Not Diabetic','Diabetic'
plt.figure(figsize=(10,7))
plt.pie(diabetes['Outcome'].value_counts(),labels=labels,colors=colors,autopct='%0.02f%%')
plt.legend()
plt.show()

#gráfico de barras para GlycemiaValues -- está a dar erro
glyval=diabetes['GlycemiaValues'].value_counts()
sns.barplot(data=diabetes, x="GlycemiaValues", y=diabetes['GlycemiaValues'].value_counts())
plt.show()

#heatmap - avaliação de possíveis correlações
sns.heatmap(data=diabetes)
plt.show(sns)
'''
