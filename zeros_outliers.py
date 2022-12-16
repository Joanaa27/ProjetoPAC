import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import statsmodels
import seaborn as sns
import matplotlib.pyplot as plt

diabetes = pd.read_csv("diabetes.csv")
diabetesdf=pd.DataFrame(diabetes)

#verificar valores nulos, NAs
print(diabetesdf.isnull().sum())

#verificar se existem zeros que não façam sentido
#visível na linha 20 , todas as variaveis apresentam 0 valores nulos

for feature in zero_features:
    zero_count = diabetesdf[diabetesdf[feature]==0][feature].count()
    print('{0} 0 number of cases {1}, percent is {2:.2f} %'.format(feature, zero_count, 100*zero_count/total_count))

"""
é possível observar que existem vários valores 0 na amostra que não fazem sentido
nomeadamente nas variaveis BMI, BloodPressure, Insulin, Glucose, SkinThickness
assim substituimos os 0 pela média dos valores das variáveis
"""

diabetesdf['BMI'] = diabetesdf['BMI'].replace(0,diabetesdf['BMI'].mean(diabetesdf['BMI']))
diabetesdf['BloodPressure'] = diabetesdf['BloodPressure'].replace(0,diabetesdf['BloodPressure'].mean(diabetesdf['BloodPressure']))
diabetesdf['Insulin'] = diabetesdf['Insulin'].replace(0,diabetesdf['Insulin'].mean(diabetesdf['Insulin']))
diabetesdf['Glucose'] = diabetesdf['Glucose'].replace(0,diabetesdf['Glucose'].mean(diabetesdf['Glucose']))
diabetesdf['SkinThickness'] = diabetesdf['SkinThickness'].replace(0,diabetesdf['SkinThickness'].mean(diabetesdf['SkinThickness']))
print(diabetesdf)

#função para remover outliers
def outlier_removal(self,dataframe):
    def outlier_limits(col):
        q3,q1 = np.nanpercentile(col,[75,25])
        IQR = q3 - q1
        UL = q3 + 1.5* IQR
        LL = q1 - 1.5* IQR
        return UL, LL
    for column in diabetesdf.columns:
        if dataframe[column].dtype!= 'int64':
            UL,LL = outlier_limits(diabetesdf[column])
            dataframe[column] = np.where(diabetesdf[column]> UL | diabetesdf[column]< LL, np.nan,diabetesdf[column])
    return dataframe

#fazer boxplot para verificação
fig , ax = plt.subplots(figsize = (20,20))
sns.boxplot(data = diabetesdf, ax = ax)


####################3
valores = []
for i in diabetesdf["GlycemiaValues"]:
    val = 0
    if i=="Hypoglycemia":
        val = 0
    elif i == "Normal":
        val = 1
    elif i== "Pre-diabetes":
        val= 2
    else:
        val= 3
    valores.append(val)

diabetesdf2=diabetesdf
diabetesdf2.insert(loc=3, column="glycvalues", value=valores)

print(diabetesdf2)

diabetesbp2= diabetesdf2.drop("Outcome", axis=1)

print(diabetesbp2)