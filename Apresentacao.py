#Importação de packages
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

print("Projeto de PAC - Base de dados 'Diabetes'")

#Leitura do ficheiro csv
diabetes = pd.read_csv("diabetes.csv")

#Visualizar o conteúdo do ficheiro csv (indica as linahs e as colunas)
print(diabetes)

#Informações acerca da base de dados (colunas, NA, tipo de variavel, etc)
diabetes.info()

#propriedades estatísticas das variáveis numéricas - temos de transformar as variaveis float em int
print(diabetes.describe())

diabetesdf=pd.DataFrame(diabetes)
print(diabetesdf)
print(diabetesdf.columns)

#verificar valores nulos, NAs
diabetesdf.isnull().sum()

#verificar se existem zeros que não façam sentido
#visível na linha 20 , todas as variaveis apresentam 0 valores nulos

#for feature in zero_features:
#    zero_count = diabetesdf[diabetesdf[feature]==0][feature].count()
#    print('{0} 0 number of cases {1}, percent is {2:.2f} %'.format(feature, zero_count, 100*zero_count/total_count))

"""
É possível observar que existem vários valores 0 na amostra que não fazem sentido
nomeadamente nas variaveis BMI, BloodPressura, Insulin, Glucose, SkinThickness
assim substituimos os 0 pela média dos valores das variáveis
"""
diabetesdf['BMI'] = diabetesdf['BMI'].replace(0,diabetesdf['BMI'].mean())
diabetesdf['BloodPressure'] = diabetesdf['BloodPressure'].replace(0,diabetesdf['BloodPressure'].mean())
diabetesdf['Insulin'] = diabetesdf['Insulin'].replace(0,diabetesdf['Insulin'].mean())
diabetesdf['Glucose'] = diabetesdf['Glucose'].replace(0,diabetesdf['Glucose'].mean())
diabetesdf['SkinThickness'] = diabetesdf['SkinThickness'].replace(0,diabetesdf['SkinThickness'].mean())
print(diabetesdf)

"""
Adicionar nova coluna na data frame: glucose medida em período pós-prandial, 2h após refeição
https://www.mayoclinic.org/tests-procedures/glucose-tolerance-test/about/pac-20394296
<70 mg/dL: hipoglicemia; 70 a 140 mg/dL: normal; 140 a 200 mg/dL: pré-diabetes; >200 mg/dL: diabetes
"""
x=[]
for i in diabetesdf["Glucose"]:
    valor = ""
    if i <= 70:
        valor = "Hypoglycemia"
    elif i <= 140:
        valor = "Normal"
    elif i <= 199:
        valor = "Pre-diabetes"
    else:
        valor = "Diabetes"
    x.append(valor)

diabetesdf.insert(loc = 2, column = "GlycemiaValues", value = x)
print(diabetesdf)
#Vai ser adicionada uma nova coluna que vai converter os valores de glucose em 4 patamares

#Palete de cores! - a palete de cores só é usada em gráfico em função do Outcome (palete1) ou dos Glycemia Values (palete2)
palete1 = {0: 'blue', 1: 'green'}
palete2 = {'Hypoglycemia': 'blue', 'Normal': 'green', 'Pre-diabetes': 'orange'}

#Gráfico de barras para a contagem de outcomes
sns.set(style = "darkgrid")
sns.countplot(data = diabetesdf, x = diabetesdf["Outcome"], palette = 'pastel', saturation = 2)
plt.title("Distribution of Outcome Values")
plt.show()

#Gráfico circular para a variável Outcome
colors = sns.color_palette('pastel')
labels = 'Non-Diabetic','Diabetic'
plt.figure(figsize = (10,7))
plt.pie(diabetes['Outcome'].value_counts(), labels = labels, colors = colors, autopct = '%0.01f%%')
plt.legend()
plt.show()

#Gráfico de barras para a GlycemiaValues
sns.set(style = "darkgrid")
sns.countplot(x = "GlycemiaValues", data = diabetesdf, order = ['Hypoglycemia','Normal','Pre-diabetes'], palette = 'pastel', saturation = 2)
plt.title('Gráfico de barras para a variável categoria GlycemiaValues')
plt.show()

#Gráfico circular para a variavel criada GlycemiaValues
colors = sns.color_palette('pastel')
labels = 'Normal', 'Pre-diabetes', 'Hypoglycemia'
plt.figure(figsize = (10,7))
plt.pie(diabetes['GlycemiaValues'].value_counts(), labels = labels, colors = colors, autopct = '%0.01f%%')
plt.legend()
plt.show()

#Histograma e boxplot para  cada variável numérica
colors = sns.color_palette('pastel')

def varnum(variavel):
    print(variavel)
    sns.histplot(data = diabetesdf, x = variavel, kde = True)
    plt.title(f"Histogram of {variavel}")
    plt.show()
    sns.boxplot(data = diabetesdf, x = variavel)
    plt.title(f"Boxplot of {variavel}")
    plt.show()

varnum("Glucose")

#Histograma de uma variavel numérica em função de uma das 2 variaveis (categoria) Outcome ou GlycemiaValues
def varhue(variavel, categoria):
    sns.histplot(data = diabetesdf, x = variavel, hue = categoria, legend = True)
    plt.title(f"Histogram of {variavel} in order to {categoria}")
    plt.show()

varhue("Glucose", "Outcome")
varhue("Glucose","GlycemiaValues")

#Função para remover outliers
def outlier_removal(self,data):
    def outlier_limits(col):
        q3,q1 = np.nanpercentile(col,[75,25])
        IQR = q3 - q1
        UL = q3 + 1.5* IQR
        LL = q1 - 1.5* IQR
        return UL, LL
    for column in data.columns:
        if data[column].dtype!= 'int64':
            UL,LL = outlier_limits(data[column])
            data[column] = np.where(data[column] > UL | data[column] < LL, np.nan,data[column])
    return data

#é suposto fazermos um gráfico novamente só para mostrar que conseguimos remover os outliers?

#fazer boxplot para verificação
fig , ax = plt.subplots(figsize = (20,20))
sns.boxplot(data = diabetesdf, ax = ax)


#Função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def varscatter(variavel_1,variavel_2):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data=diabetesdf, x=variavel_1, y=variavel_2)
    plt.title(f"Scatterplot of {variavel_1} by {variavel_2}")
    plt.show()

varscatter("Glucose","BMI")

#caso o utilizador opte por fazer em função ou do outcome ou da variavel "GlycemiaValues" incorporar esta função
def varscatter2(variavel1, variavel2, varcategorical):
    sns.scatterplot(data=diabetesdf, x=variavel1, y=variavel2, hue=varcategorical)
    plt.title(f"Scatterplot of {variavel1} by {variavel2} in order to {varcategorical}")
    plt.show()

varscatter2("Glucose","BMI","Outcome")
varscatter2("Glucose","BMI","GlycemiaValues")

#Pairplot
plt.figure()
sns.set(font_scale=0.7, style="darkgrid")
sns.pairplot(diabetesdf, hue = "Outcome", diag_kind = "kde", palette = palete1, plot_kws = {"s": 8})
plt.title('Pairplot')
plt.show()

#matriz de graficos de dispersão que inclui todas as variaveis - tenho de melhorar
sns.set_theme(style="ticks")
sns.pairplot(diabetesdf, hue="Outcome")
plt.show()

#Matriz de correlações
corr = diabetesdf.corr().round(2)
plt.figure(figsize=(14, 10))
sns.set(font_scale=1.15)
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
sns.heatmap(corr, annot = True, cmap = 'BuPu', mask = mask, cbar = True)
plt.title('Matriz de correlações')
plt.show()