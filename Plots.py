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

#heatmap - avaliação de possíveis correlações
# Create a pivot table
matriz=diabetesdf.pivot("Pregnancies", "Glucose", "BloodPressure")
sns.heatmap(matriz, annot=True, fmt=".1f")
plt.show()

#separam o outcome 0 de 1
df_d0 = diabetes[diabetes['Outcome'] == 0]
df_d1 = diabetes[diabetes['Outcome'] == 1]

#and random sample the same amount of instances from the higher represented '0' class to match the available '1' class instances
df_d0_samp = df_d0.sample(268,replace = False)
df_bal = pd.concat([df_d1, df_d0_samp])

#histograma com função de densidade da variável Pregnancies, BMI e DiabetesPedigreeFunction
cores = {0: 'blue', 1: 'green'}
counter = 0
for i in variaveis:
    counter += 1
    print(counter, ':', i)
    sns.displot(data = df_bal, kde=True, x = diabetes[str(i)], hue='Outcome', palette=cores)
    plt.title(f'"{i}" em função do Outcome')
plt.plot()
plt.show()



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

