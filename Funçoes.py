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
print(diabetesdf)

#análise para cada variável numérica, breve descrição estatística (média, quartis, etc) e histograma para observar a distribuição4
colors = sns.color_palette('pastel')

print(diabetesdf.loc[2])
"""
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

#esta função permite ao utilizador escolher visualizar um histograma de uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
def varhue(variavel, categoria):
    sns.histplot(data=diabetesdf, x=variavel, hue= categoria, legend=True)
    plt.title(f"Histogram of {variavel} in order to {categoria}")
    plt.show()

varhue("Glucose", "Outcome")
varhue("Glucose","GlycemiaValues")

#função para efetuar boxplots de uma variavel numérica em função de uma das 2 variaveis(categoria) Outcome ou GlycemiaValues
#def varboxplot (variavel,categoria):
#    sns.boxplot(data=diabetesdf, x=variavel, y=categoria,hue=categoria, dodge=False)
#    plt.show()

#varboxplot("Glucose","Outcome")


#boxplot de todas as variáveis em função da variavel "Outcome"
#eliminar a coluna GlycemiaValues porque não queremos e não faz sentido aparecer na data frame
diabetesbp= diabetesdf.drop("GlycemiaValues", axis=1)

diabetes_melted = pd.melt(diabetesbp, id_vars = "Outcome", var_name = "variables", value_name = "value")

plt.figure(figsize = (15, 15))
sns.boxplot(data = diabetes_melted, x="variables", y="value", hue="Outcome")
plt.title("Boxplot of all numeric variables in order to Outcome")
plt.show()


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

print("diabetesdf2")
print(diabetesdf2)

diabetesbp2= diabetesdf2.drop("Outcome", axis=1)

print("diabetesbp2")
print(diabetesbp2)

diabetes_melt= pd.melt(diabetesbp2, id_vars = "glycvalues", var_name = "variables", value_name = "value")

print("diabetesmelt")
print(diabetes_melt)
#em função de GlycemiaValues
plt.figure(figsize = (15, 15))
sns.boxplot(data = diabetes_melt, x="variables", y="value", hue="glycvalues")
plt.title("Boxplot of all numeric variables in order to GlycemiaValues")
plt.show()

#swarm plot
plt.figure(figsize = (15, 15))
sns.swarmplot(x = "variables", y = "value", hue = "Outcome", data = diabetes_melted)
plt.show()

#função que executa gráficos de dispersão entre as variaveis NUMERICAS escolhidas pelo utilizador
def varscatter(variavel_1,variavel_2):
    print(f"Variável no eixo dos xx: {variavel_1} \nVariável no eixo dos yy: {variavel_2}")
    sns.scatterplot(data=diabetesdf, x=variavel_1, y=variavel_2)
    plt.title(f"Scatterplot of {variavel_2} by {variavel_1}")
    plt.show()

varscatter("Glucose","BMI")
varscatter("DiabetesPedigreeFunction","Outcome")

#caso o utilizador opte por fazer em função ou do outcome ou da variavel "GlycemiaValues" incorporar esta função
def varscatter2(variavel1, variavel2, varcategorical):
    sns.scatterplot(data=diabetesdf, x=variavel1, y=variavel2, hue=varcategorical)
    plt.title(f"Scatterplot of {variavel2} by {variavel1} in order to {varcategorical}")
    plt.show()

varscatter2("Glucose","BMI","Outcome")
varscatter2("Glucose","BMI","GlycemiaValues")

#matriz de graficos de dispersão que inclui todas as variaveis - tenho de melhorar
def scattermat (vcategorical):
    sns.set_theme(style="ticks")
    order = []
    if vcategorical=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    sns.pairplot(diabetesdf, hue= vcategorical, hue_order=order)
    plt.show()

scattermat("GlycemiaValues")
scattermat("Outcome")

#o hue nao consegue interpretar a variavel "GlycemiaValues" temos de fazer um dicionario
#Glycemia_Values = {"Hypoglycemia": 0, "Normal": 1, "Pre-diabetes": 2}
#print(Glycemia_Values)

#histograma e função densididade para cada uma das variaveis em função do "Outcome" e "GlycemiaValues" => tentar alterar pallete
def variaveiscat(variavel , categoria):
    if categoria=="Outcome":
        order=[0,1]
    else:
        order=['Hypoglycemia','Normal','Pre-diabetes']
    sns.histplot(data=diabetesdf, x=variavel,kde=True, hue=categoria, hue_order=order)
    plt.title(f"Histogram of {variavel} by {categoria}")
    plt.show()

variaveiscat("Age","Outcome")
variaveiscat("Insulin","GlycemiaValues")

#histograma e função densididade de TODAS as variaveis em função do "Outcome" e "GlycemiaValues"
counter = 0
for i in variaveis:
    counter += 1
    print(counter, ':', i)
    plt.subplot(3, 3, counter)
    sns.histplot(data = diabetesdf, x = diabetesdf[str(i)], hue = "Outcome", multiple  = 'dodge', kde=True)
plt.suptitle("Histogram of all variables by Outcome", fontsize=16)
plt.plot()
plt.show()

##### NÃO ESTÁ A FUNCIONAR #####

counter = 0
for i in variaveis:
    counter += 1
    print(counter, ':', i)
    plt.subplot(3, 3, counter)
    sns.boxplot(data = diabetesdf, x = diabetesdf[str(i)], y="Outcome", dodge=False)
plt.suptitle("Boxplot of all variables by Outcome", fontsize=16)
plt.plot()
plt.show()

if categoria=="Outcome":
    order=[0,1]
else:
    order=['Hypoglycemia','Normal','Pre-diabetes']
sns.histplot(data=diabetesdf, x=variaveis,kde=True, hue=categoria, hue_order=order)
"""

df_d0 = diabetesdf[diabetesdf['Outcome'] == 0]
df_d1 = diabetesdf[diabetesdf['Outcome'] == 1]

#and random sample the same amount of instances from the higher represented '0' class to match the available '1' class instances
df_d0_samp = df_d0.sample(264,replace = False) # this time 264 is the sample number for reason as we see above
df_bal = pd.concat([df_d1, df_d0_samp]) #putting back the two class together

def regressao (variavel1,variavel2):
    sns.regplot(x=variavel1, y=variavel2, data=df_bal[df_bal['Outcome'] == 0], color='blue')
    sns.regplot(x=variavel1, y=variavel2, data=df_bal[df_bal['Outcome'] == 1], color='red')
    plt.title(f"{variavel1} vs {variavel2} scatterplot")
    plt.show()

regressao("Glucose","Age")

def catplotvar(variavel):
    sns.catplot(x = "Outcome", y = variavel, hue = "Outcome", kind = "swarm", data = diabetesdf)
    plt.show()

catplotvar("BMI")