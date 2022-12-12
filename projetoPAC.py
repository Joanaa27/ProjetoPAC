import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn
import matplotlib

print("Projeto de PAC - Base de dados 'Diabetes'")

#ler o ficheiro csv
diabetes = pd.read_csv("diabetes.csv")

#visualizar o conteúdo do ficheiro csv (indica as linahs e as colunas)
print(diabetes)

#informações acerca da base de dados (colunas, NA, tipo de variavel, etc)
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

for feature in zero_features:
    zero_count = diabetesdf[diabetesdf[feature]==0][feature].count()
    print('{0} 0 number of cases {1}, percent is {2:.2f} %'.format(feature, zero_count, 100*zero_count/total_count))

"""
é possível observar que existem vários valores 0 na amostra que não fazem sentido
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

#função para remover outliers
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
            data[column] = np.where(data[column]> UL | data[column]< LL, np.nan,data[column])
    return data

#fazer boxplot para verificação
fig , ax = plt.subplots(figsize = (20,20))
sns.boxplot(data = diabetesdf, ax = ax)



########### Opções do utilizador ##########
opcao= int(input("Escolha uma categoria para a análise que pretende \n 0-Overview \n 1-Variables \n 2-Interaction \n 3-Correlations \n 4-Missing Values \n 5-Sample \n 6-Report \n Opção:  "))
while opcao <0 and opcao >= 6:
    print("Tem de escolher uma opção entre 0 e 6")
    opcao= int(input("Escolha a 2opção que deseja \n 0-Overview \n 1-Variables \n 2-Interaction \n 3-Correlations \n 4-Missing Values \n 5-Sample \n 6-Report \n Opção:  "))

#opção 0 - visualização da data frame e de algumas informações relativas à mesma
if opcao == 0:
    print(diabetesdf)
    diabetesdf.info()
elif opcao == 1:
    variavel= int(input("Escolha uma das seguintes opções:\n 0-Análise Geral das Variáveis Numéricas \n 1- "))
    if variavel==0:
        print(diabetesdf.describe())
    elif variavel==1:
        print("xau")
#elif opcao == 2:
#    função3
#elif opcao == 3:
#    função4
elif opcao == 6:
    #geração de um relatório automático sobre a analise da base de dados
    relatorio = ProfileReport(diabetesdf, title="Data Analysis of Diabetes Report")
    diabetesdf.profile_report()
    relatorio.to_file("diabetes_report.html")
#else:

#se quiser ir buscar certas observações com x condição usar:
diabetesdf.loc[diabetesdf["Outcome"=="0"]]