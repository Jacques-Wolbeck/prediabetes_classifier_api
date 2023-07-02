import pandas as pd
import numpy as np
import joblib
import gzip




database = pd.read_csv('data/diabetes_012_health_indicators_BRFSS2015.csv')


"""## **Pré-processamento dos Dados**"""

#transformando os dados em inteiros
database["Diabetes_012"] = database["Diabetes_012"].astype(int)
database["HighBP"] = database["HighBP"].astype(int)
database["HighChol"] = database["HighChol"].astype(int)
database["CholCheck"] = database["CholCheck"].astype(int)
database["BMI"] = database["BMI"].astype(int)
database["Smoker"] = database["Smoker"].astype(int)
database["Stroke"] = database["Stroke"].astype(int)
database["HeartDiseaseorAttack"] = database["HeartDiseaseorAttack"].astype(int)
database["PhysActivity"] = database["PhysActivity"].astype(int)
database["Fruits"] = database["Fruits"].astype(int) 
database["Veggies"] = database["Veggies"].astype(int)
database["HvyAlcoholConsump"] = database["HvyAlcoholConsump"].astype(int)
database["AnyHealthcare"] = database["AnyHealthcare"].astype(int)
database["NoDocbcCost"] = database["NoDocbcCost"].astype(int)
database["GenHlth"] = database["GenHlth"].astype(int)
database["MentHlth"] = database["MentHlth"].astype(int)
database["PhysHlth"] = database["PhysHlth"].astype(int)
database["DiffWalk"] = database["DiffWalk"].astype(int)
database["Sex"] = database["Sex"].astype(int)
database["Age"] = database["Age"].astype(int)
database["Education"] = database["Education"].astype(int)
database["Income"] = database["Income"].astype(int)

database.loc[database['Diabetes_012'] == 2, 'Diabetes_012'] = np.nan
database.dropna(inplace = True)
database.rename(columns={"Diabetes_012":"Diabetes_binary"}, inplace = True)

"""As linhas onde 'Diabetes_012' eram igual a 2 foram descartadas, pois só analisaremos os casos onde o paciente não tem diabetes(0) ou é pré-diabético(1)"""



#excluindo os dados duplicados
database.drop_duplicates(inplace = True)

#Diminuindo um pouco o dataset em relação a classe 'No Diabetes'
database = pd.concat([database[database.Diabetes_binary == 0].sample(frac = 0.1) , database[database.Diabetes_binary == 1]])


"""# **Aprendizado de Máquina** """

#separando os dados em 'features' e 'target' para usar nos algoritmos de classificação
features = ['GenHlth',
            'HighBP',
            'HighChol',
            'BMI',
            'Income',
            'DiffWalk',
            'Age',
            'PhysHlth',
            'Education',
            'HeartDiseaseorAttack',
            'PhysActivity',
            'MentHlth',
            'CholCheck',
    
]

target = ['Diabetes_binary']

X = database[features]
y = database[target]

X.isnull().sum()

#from imblearn.under_sampling import RandomUnderSampler, NearMiss
from imblearn.over_sampling import SMOTE, RandomOverSampler
'''como os dados estão bastante desbalaceados, será realizada a estratégia de over sampling conhecida como SMOTE(Synthetic Minority Over-sampling Technique), ou seja, serão gerados novas instâncias sintéticas da classe minoritária 
afim de equilibrar com a quantidade de dados das pessoas não diabéticas (classe majoritária)'''

#rus = RandomUnderSampler(sampling_strategy='majority', random_state = 0)
#X_under, y_under = rus.fit_resample(X, y)

#nm = NearMiss(version = 1, n_neighbors = 10)
#X_under, y_under = nm.fit_resample(X, y)

#ros = RandomOverSampler(random_state=42)
#X_over, y_over = ros.fit_resample(X, y)

sm = SMOTE(random_state = 42)
X_smote, y_smote = sm.fit_resample(X, y)



#separando o dataset em dados de treino e de teste
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X_smote, y_smote, test_size = 0.25, random_state = 42)

#padronizando os dados de treino e teste
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve


"""É possivel notar que o classificador com maior desempenho foi o 'Random Forest', agora iremos analisar mais afundo os dados, utilizando este modelo de classificação"""

#Gerando a matriz de confusão, baseado no algoritmo de classificação Random Forest
best_model = RandomForestClassifier()
best_model.fit(X_train, y_train.values.ravel())

#y_pred = best_model.predict(X_test)


joblib.dump(best_model, gzip.open('model/model_binary.dat.gz', "wb"))